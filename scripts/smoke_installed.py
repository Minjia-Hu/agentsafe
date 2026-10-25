"""Exercise the installed wheel outside a checkout, using fictional inputs only."""

import base64
from http.client import HTTPConnection
from importlib.resources import files
from io import BytesIO
import json
from pathlib import Path
import threading
import time

import agentsafe
from agentsafe.extract import check_ocr
from agentsafe.gui import LocalServer
from agentsafe.redaction import FILL
from PIL import Image


def main():
    source_root = Path(__file__).resolve().parents[1] / "src"
    if Path(agentsafe.__file__).resolve().is_relative_to(source_root):
        raise SystemExit("Run with a separately installed wheel, without source PYTHONPATH.")
    check_ocr()  # Missing OCR is a failure, not a skipped packaging check.
    server = LocalServer()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    def request(route, *, body=None, authenticated=True):
        headers = {"Host": server.host_header}
        if authenticated:
            headers["X-AgentSafe-Session"] = server.session.token
        if body is not None:
            headers["Content-Type"] = "application/json"
        connection = HTTPConnection("127.0.0.1", server.server_port, timeout=5)
        try:
            connection.request("POST" if body is not None else "GET", route, body, headers)
            response = connection.getresponse()
            return response.status, response.read()
        finally:
            connection.close()

    def finished():
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            code, data = request("/api/status")
            assert code == 200
            result = json.loads(data)
            if result["state"] != "running":
                assert result["state"] == "done" and result["incomplete"] == 0
                return result
            time.sleep(.05)
        raise AssertionError("Synthetic installed-wheel scan timed out.")

    try:
        for route in ("/", "/gui.js", "/redaction.js", "/redaction.css", "/icons/monogram.svg", "/favicon.ico"):
            code, data = request(route, authenticated=False)
            assert code == 200 and data, route
        assert request("/api/status", authenticated=False)[0] == 401
        assert request("/api/demo/terms", body=b"")[0] == 202
        original = finished()
        assert original["high"] > 0 and original["policy_counts"]["terms"] == 3
        source = files("agentsafe").joinpath("demo_assets/business-context.png").read_bytes()
        with Image.open(BytesIO(source)) as image:
            width, height = image.size
        # A full cover is deterministic across OCR versions. Pixel tests for
        # partial covers remain in the behavior suite; this checks wheel wiring.
        payload = json.dumps({"review_id": original["review_id"], "image_index": 0,
                              "regions": [{"x": 0, "y": 0, "w": width, "h": height}]}).encode()
        assert request("/api/redact", body=payload)[0] == 202
        copy = finished()
        assert copy["redacted"] and copy["total"] == 1
        assert copy["policy_counts"] == original["policy_counts"]
        assert copy["manual_review"] == 1  # A blank cover is not a privacy pass.
        assert copy["export"]["name"] == "business-context-redacted.png"
        with Image.open(BytesIO(base64.b64decode(copy["export"]["url"].split(",", 1)[1]))) as image:
            assert image.mode == "RGB" and image.size == (width, height)
            assert image.getextrema() == tuple((channel, channel) for channel in FILL)
        assert request("/api/clear", body=b"")[0] == 200
        assert json.loads(request("/api/status")[1])["state"] == "idle"
        print(f"Installed AgentSafe {agentsafe.__version__}: assets, auth, synthetic GUI scan, PNG copy/recheck and clear passed.")
    finally:
        server.session.close()
        server.shutdown()
        server.server_close()
        thread.join(5)


if __name__ == "__main__":
    main()
