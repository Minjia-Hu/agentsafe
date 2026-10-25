"""Real loopback boundary and GUI workflow tests with fictional inputs only."""

from http.client import HTTPConnection
import json
import base64
import hashlib
from importlib.resources import files
from io import BytesIO
import re
import socket
import struct
import threading
import time

import pytest
from PIL import Image

from agentsafe.config import Policy
from agentsafe.extract import check_ocr
from agentsafe.gui import LocalServer, UPLOAD_BYTES, decode_upload
from agentsafe.models import Limits, ScanError
from agentsafe.scan import scan_buffers
from agentsafe.redaction import FILL

ORIGINAL_CONNECT = socket.socket.connect


def selection(inputs, *, domains=(), cookies=(), terms=(), lang="zh"):
    header = json.dumps({
        "files": [{"name": name, "size": len(data)} for name, data in inputs],
        "policy": {"sensitive_domains": list(domains), "session_cookie_names": list(cookies), "sensitive_terms": list(terms)}, "lang": lang,
    }).encode()
    return struct.pack("!I", len(header)) + header + b"".join(data for _, data in inputs)


@pytest.fixture
def local_gui(monkeypatch):
    # All older scanner tests still forbid network access. This suite allows
    # only an exact local connection to its own ephemeral GUI server.
    server = LocalServer(lang="zh")
    def connect(sock, address):
        if address != ("127.0.0.1", server.server_port):
            raise AssertionError("Only this test's local GUI connection is allowed")
        return ORIGINAL_CONNECT(sock, address)
    monkeypatch.setattr(socket.socket, "connect", connect)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield server
    server.shutdown()
    server.server_close()
    thread.join(2)


def request(server, route, *, method="GET", data=None, auth=True, origin=None, host=None, extra=None):
    connection = HTTPConnection("127.0.0.1", server.server_port, timeout=5)
    # Avoid socket.create_connection, which remains forbidden everywhere.
    connection.sock = socket.socket()
    connection.sock.settimeout(5)
    connection.sock.connect(("127.0.0.1", server.server_port))
    headers = {"Host": host or server.host_header}
    if auth:
        headers["X-AgentSafe-Session"] = server.session.token
    if origin:
        headers["Origin"] = origin
    if data is not None:
        headers["Content-Type"] = "application/octet-stream"
    headers.update(extra or {})
    connection.request(method, route, body=data, headers=headers)
    response = connection.getresponse()
    status, response_headers, body = response.status, dict(response.getheaders()), response.read()
    connection.close()
    return status, response_headers, body


def finished(server):
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        status, _, data = request(server, "/api/status")
        assert status == 200
        result = json.loads(data)
        if result["state"] != "running":
            return result
        time.sleep(.02)
    pytest.fail("Local scan did not finish within the test budget")


def test_browser_snapshots_use_existing_rules_and_coverage():
    inputs = [
        ("session.log", b"Authorization: Bearer SYNTHETIC_NOT_A_VALID_TOKEN\nCookie: auth_session=FICTIONAL_VALUE\nhttps://console.northstar.test"),
        ("unsupported.pdf", b"fictional"),
        ("invalid.txt", b"\xff"),
    ]
    report = scan_buffers(inputs, Policy(("northstar.test",), ("auth_session",)))
    assert len(report.files) == 3
    assert [item.coverage for item in report.files] == ["inspected", "uninspected", "failed"]
    assert [f.line for f in report.files[0].findings] == [1, 2, 3]
    assert report.exit_code == 2
    assert "SYNTHETIC_NOT_A_VALID_TOKEN" not in repr(report)
    limited = scan_buffers([("large.txt", b"abcdef")], Policy(), limits=Limits(text_bytes=2))
    assert limited.exit_code == 2


def test_selection_framing_and_policy():
    inputs = [("session.log", b"fictional"), ("same.log", b""), ("same.log", b"another")]
    decoded, policy, lang = decode_upload(selection(inputs, domains=("Northstar.test",)))
    assert decoded == inputs and policy.sensitive_domains == ("northstar.test",) and lang == "zh"
    with pytest.raises(ScanError):
        decode_upload(selection(inputs, domains=("https://private.test",)))
    with pytest.raises(ScanError):
        decode_upload(selection(inputs) + b"unexpected")
    with pytest.raises(ScanError):
        decode_upload(selection(inputs)[:-1])


@pytest.mark.parametrize("name", ["../private.log", "https://private.test/x", "C:\\private.log", "nul\x00.log"])
def test_gui_rejects_paths_and_urls(name):
    with pytest.raises(ScanError):
        decode_upload(selection([(name, b"fictional")]))


def test_reject_excessive_selection():
    with pytest.raises(ScanError):
        decode_upload(selection([(f"{i}.txt", b"") for i in range(21)]))
    with pytest.raises(ScanError):
        decode_upload(struct.pack("!I", 65537) + b"{}")


def test_local_page_is_private_and_has_no_filesystem_routes(local_gui):
    server = local_gui
    assert server.server_address[0] == "127.0.0.1"
    code, headers, data = request(server, "/", auth=False)
    assert code == 200 and b'<html lang="zh">' in data
    assert headers["Cache-Control"] == "no-store"
    assert "connect-src 'self'" in headers["Content-Security-Policy"]
    assert "frame-ancestors 'none'" in headers["Content-Security-Policy"]
    assert server.session.token.encode() not in data
    for route in ("/api/status", "/api/info", "/../README.md", "/.env"):
        assert request(server, route, auth=False)[0] == 401
    assert request(server, "/../README.md")[0] == 404
    assert request(server, "/gui.js", auth=False)[0] == 200


def test_auth_host_origin_and_request_bounds(local_gui):
    server = local_gui
    payload = selection([("fictional.log", b"fictional")])
    for kwargs in (
        {"auth": False}, {"origin": "https://untrusted.test"}, {"host": "untrusted.test"},
        {"origin": "null"}, {"extra": {"Sec-Fetch-Site": "cross-site"}},
        {"extra": {"X-AgentSafe-Session": "not-the-session"}},
        {"extra": {"X-AgentSafe-Session": "\xe9"}},
    ):
        assert request(server, "/api/scan", method="POST", data=payload, **kwargs)[0] in (401,403)
    assert server.session.status()["state"] == "idle"
    assert request(server, "/api/scan", method="POST", data=b"not a selection")[0] == 400
    assert request(server, "/api/scan", method="POST", data=b"", extra={"Content-Length":str(UPLOAD_BYTES + 65541)})[0] == 400
    assert request(server, "/api/scan", method="POST", data=payload, extra={"Content-Type":"text/plain"})[0] == 400
    assert server.session.status()["state"] == "idle"


def test_only_authenticated_api_requests_extend_idle_lifetime(local_gui):
    server = local_gui
    server.session.last_activity = 1.0
    for route in ("/", "/gui.js", "/favicon.ico"):
        assert request(server, route, auth=False)[0] == 200
        assert server.session.last_activity == 1.0
    assert request(server, "/api/status", auth=False)[0] == 401
    assert request(server, "/api/status", origin="https://outside.test")[0] == 403
    assert server.session.last_activity == 1.0
    assert request(server, "/api/status")[0] == 200
    assert server.session.last_activity > 1.0


def test_scan_clear_rescan_and_stop(local_gui):
    server = local_gui
    raw = b"Authorization: Bearer SYNTHETIC_NOT_A_VALID_TOKEN\nCookie: preference=dark"
    code, _, data = request(server, "/api/scan", method="POST", data=selection([("session.log", raw)]), origin=server.origin)
    assert code == 202
    result = finished(server)
    assert result["high"] == 1 and result["warn"] == 1 and result["incomplete"] == 0
    assert result["exit_code"] == 1 and "第 1 行" in result["cards"]
    assert "SYNTHETIC_NOT_A_VALID_TOKEN" not in result["cards"] and "preference=dark" not in result["cards"]
    assert "脱敏日志预览" in result["cards"] and "Authorization:" in result["cards"] and "preference=" in result["cards"]
    assert 'data-target="scan-f0-line-1"' in result["cards"]
    assert request(server, "/api/clear", method="POST")[0] == 200
    assert server.session.status() == {"state":"idle"}
    assert request(server, "/api/scan", method="POST", data=selection([("reviewed.log", b"Authorization: [REDACTED]")]))[0] == 202
    result = finished(server)
    assert result["high"] == 0 and result["exit_code"] == 0
    assert request(server, "/api/stop", method="POST")[0] == 200
    assert server.session.closed and server.session.job is None and server.session.token == ""
    assert request(server, "/api/status", auth=False)[0] == 401


def test_every_requested_file_accounted_for_and_names_escaped(local_gui):
    server = local_gui
    payload = selection([("bad.pdf", b"fictional"), ("<img onerror=bad>.txt", b"\xff"), ("okay.txt", b"public fictional example")])
    assert request(server, "/api/scan", method="POST", data=payload)[0] == 202
    result = finished(server)
    assert result["total"] == 3 and result["incomplete"] == 2 and result["exit_code"] == 2
    assert "&lt;img onerror=bad&gt;.txt" in result["cards"] and "<img onerror=bad>" not in result["cards"]


def test_only_one_scan_can_reserve_the_session(local_gui):
    server = local_gui
    assert server.session.reserve()
    assert request(server, "/api/demo/before", method="POST")[0] == 409
    assert request(server, "/api/clear", method="POST")[0] == 409
    server.session.release()
    assert request(server, "/api/clear", method="POST")[0] == 200


@pytest.mark.ocr
def test_real_image_gui_demo_and_manual_review(local_gui):
    try:
        check_ocr()
    except ScanError as error:
        pytest.skip(str(error))
    server = local_gui
    assert request(server, "/api/demo/before", method="POST")[0] == 202
    result = finished(server)
    assert result["state"] == "done" and result["synthetic"]
    assert result["high"] == 4 and result["warn"] == 2 and result["incomplete"] == 0
    assert 'data:image/png;base64,' in result["cards"] and 'data-target=' in result["cards"]
    assert request(server, "/api/demo/miss", method="POST")[0] == 202
    result = finished(server)
    assert result["manual_review"] == 1 and result["high"] == result["warn"] == 0
    assert "未识别出文字，需人工检查图片" in result["cards"] and "CHECKED" not in result["cards"]


def test_missing_ocr_never_becomes_a_clean_image_result(local_gui, monkeypatch):
    def unavailable():
        raise ScanError("Tesseract was not found. Install it and add it to PATH, or set AGENTSAFE_TESSERACT.")
    monkeypatch.setattr("agentsafe.extract.tesseract_command", unavailable)
    server = local_gui
    assert request(server, "/api/demo/before", method="POST")[0] == 202
    result = finished(server)
    assert result["incomplete"] == 1 and result["exit_code"] == 2
    assert result["high"] == 3 and result["warn"] == 1
    assert "Tesseract was not found" in result["cards"]


def test_gui_term_settings_mask_values_and_change_results(local_gui):
    server = local_gui
    raw = "Customer: 华星演示客户\nProject: Project Cedar\nPublic project: Cedarwood".encode()
    payload = selection([("context.log", raw)], terms=("华星演示客户", "Project Cedar"))
    assert request(server, "/api/scan", method="POST", data=payload)[0] == 202
    result = finished(server)
    assert result["high"] == 2 and result["warn"] == 0 and result["exit_code"] == 1
    assert result["policy_counts"] == {"terms": 2, "domains": 0, "cookies": 0}
    assert "第 1 行" in result["cards"] and "第 2 行" in result["cards"]
    assert "敏感词或短语" in result["cards"]
    assert "华星演示客户" not in result["cards"] and "Project Cedar" not in result["cards"]
    assert request(server, "/api/scan", method="POST", data=selection([("context.log", raw)]))[0] == 202
    assert finished(server)["high"] == 0
    assert request(server, "/api/scan", method="POST", data=selection([("context.log", raw)], terms=("x",)))[0] == 400


@pytest.mark.ocr
def test_business_sample_checks_names_without_domains(local_gui):
    try:
        check_ocr()
    except ScanError as error:
        pytest.skip(str(error))
    assert request(local_gui, "/api/demo/terms", method="POST")[0] == 202
    result = finished(local_gui)
    assert result["state"] == "done" and result["synthetic"]
    assert result["high"] == 5 and result["warn"] == result["incomplete"] == 0
    assert result["policy_counts"] == {"terms": 3, "domains": 0, "cookies": 0}
    assert 'data-target=' in result["cards"] and "第 4 行" in result["cards"]


def redact_request(server, result, regions, *, index=0, **kwargs):
    body = json.dumps({"review_id": result["review_id"], "image_index": index, "regions": regions}).encode()
    return request(server, "/api/redact", method="POST", data=body, extra={"Content-Type": "application/json"}, **kwargs)


@pytest.mark.ocr
def test_gui_manual_copy_rechecks_exact_bytes_with_original_policy(local_gui, monkeypatch):
    try:
        check_ocr()
    except ScanError as error:
        pytest.skip(str(error))
    server = local_gui
    source = files("agentsafe").joinpath("demo_assets", "business-context.png").read_bytes()
    digest = hashlib.sha256(source).digest()
    assert request(server, "/api/demo/terms", method="POST")[0] == 202
    original = finished(server)
    # Keep one configured phrase visible, proving context is reused rather than
    # cleared when the user never entered any settings in the form.
    boxes = re.findall(r'<rect[^>]* x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)"', original["cards"])
    assert len(boxes) == 2
    x, y, w, h = map(int, boxes[0])
    region = {"x": x-4, "y": y-4, "w": w+8, "h": h+8}
    seen = []
    core = scan_buffers
    def recording(inputs, policy, **kwargs):
        seen.extend((name, data, policy) for name, data in inputs)
        return core(inputs, policy, **kwargs)
    monkeypatch.setattr("agentsafe.gui.scan_buffers", recording)
    assert redact_request(server, original, [region])[0] == 202
    result = finished(server)
    assert result["redacted"] and result["total"] == 1 and result["incomplete"] == 0
    assert result["high"] == 1 and result["policy_counts"] == original["policy_counts"]
    exported = base64.b64decode(result["export"]["url"].split(",", 1)[1])
    assert seen[0][0] == result["export"]["name"] == "business-context-redacted.png"
    assert seen[0][1] == exported and seen[0][2].sensitive_terms == ("Project Cedar", "Acme Training", "华星演示客户")
    assert hashlib.sha256(source).digest() == digest
    with Image.open(BytesIO(exported)) as image:
        assert image.mode == "RGB"
        for px in range(x, x+w):
            for py in range(y, y+h):
                assert image.getpixel((px, py)) == FILL
    assert redact_request(server, original, [region])[0] == 400
    assert request(server, "/api/clear", method="POST")[0] == 200
    assert server.session.review_images == {} and server.session.review_policy is None
    assert server.session.status() == {"state": "idle"}


@pytest.mark.ocr
def test_redaction_auth_validation_and_missing_ocr_are_honest(local_gui, monkeypatch):
    try:
        check_ocr()
    except ScanError as error:
        pytest.skip(str(error))
    server = local_gui
    assert request(server, "/api/demo/before", method="POST")[0] == 202
    original = finished(server)
    region = {"x": 10, "y": 10, "w": 30, "h": 20}
    assert redact_request(server, original, [region], auth=False)[0] == 401
    assert redact_request(server, original, [region], origin="https://outside.test")[0] == 403
    assert redact_request(server, original, [region], index=1)[0] == 400  # log, not image
    assert redact_request(server, original, [dict(region, x=True)])[0] == 400
    assert redact_request(server, original, [dict(region, w=100000)])[0] == 400
    assert request(server, "/api/redact", method="POST", data=b"not JSON", extra={"Content-Type": "application/json"})[0] == 400
    assert request(server, "/api/redact", method="POST", data=b"{}", extra={"Content-Type": "application/json", "Content-Length": "65537"})[0] == 400
    assert server.session.status()["review_id"] == original["review_id"]
    def unavailable():
        raise ScanError("Tesseract was not found; reopen the scanner after installation.")
    monkeypatch.setattr("agentsafe.extract.tesseract_command", unavailable)
    assert redact_request(server, original, [region])[0] == 202
    result = finished(server)
    assert result["exit_code"] == 2 and result["incomplete"] == 1 and result["export"]
    assert server.session.review_images == {}  # Failed scan cannot be edited as if inspected.
    server.session.close()
    assert server.session.review_policy is None and server.session.job is None


def test_closed_session_never_retains_new_inputs(local_gui):
    server = local_gui
    server.session.close()
    inputs = [("private.txt", b"SYNTHETIC_TRANSIENT_CANARY")]
    server.session.start(inputs, Policy(), "en")
    assert not inputs and server.session.job is None and not server.session.review_images


def test_browser_logo_assets_are_packaged_and_local(local_gui):
    server = local_gui
    assert request(server, "/brand")[0] == 404
    for variant in ("monogram",):
        code, headers, svg = request(server, f"/icons/{variant}.svg", auth=False)
        assert code == 200 and headers["Content-Type"] == "image/svg+xml"
        assert b"<svg" in svg and b"href=" not in svg
        code, headers, png = request(server, f"/icons/{variant}-32.png", auth=False)
        assert code == 200 and headers["Content-Type"] == "image/png"
        with Image.open(BytesIO(png)) as icon:
            assert icon.size == (32, 32)
        code, headers, ico = request(server, f"/icons/{variant}.ico", auth=False)
        assert code == 200 and headers["Content-Type"] == "image/x-icon"
        with Image.open(BytesIO(ico)) as icon:
            assert icon.info["sizes"] == {(16, 16), (32, 32), (48, 48)}
    assert request(server, "/icons/../../README.md")[0] == 404
