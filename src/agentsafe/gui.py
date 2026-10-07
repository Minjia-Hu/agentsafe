"""Session-only browser UI on an authenticated IPv4 loopback server.

The GUI accepts explicit file bytes, never paths or URLs. No artifacts are
written to disk, no filesystem is served and no external requests are made.
"""

import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
import json
import secrets
import struct
import threading
import time
import webbrowser

from .config import Policy, validate_policy
from .extract import check_ocr
from .models import Limits, ScanError
from .output import safe_path
from .preview import no_readable_text, render_cards
from .scan import scan_buffers

UPLOAD_BYTES = 24 * 1024 * 1024
HEADER_BYTES = 64 * 1024
IDLE_SECONDS = 30 * 60
CSP = "default-src 'none'; script-src 'self'; style-src 'self'; img-src data:; connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
ASSETS = {
    "/": ("gui.html", "text/html; charset=utf-8"),
    "/gui.js": ("gui.js", "text/javascript; charset=utf-8"),
    "/gui.css": ("gui.css", "text/css; charset=utf-8"),
    "/preview.js": ("preview.js", "text/javascript; charset=utf-8"),
    "/preview.css": ("preview.css", "text/css; charset=utf-8"),
}


def decode_upload(body: bytes) -> tuple[list[tuple[str, bytes]], Policy, str]:
    """Four-byte big-endian JSON length, JSON metadata, then file snapshots."""
    if len(body) < 4 or len(body) > UPLOAD_BYTES + HEADER_BYTES + 4:
        raise ScanError("Invalid or oversized selection. Select at most 24 MiB in total.")
    length = struct.unpack("!I", body[:4])[0]
    if not 0 < length <= HEADER_BYTES or length + 4 > len(body):
        raise ScanError("File selection metadata is invalid; no scan was started.")
    try:
        metadata = json.loads(body[4:4 + length])
    except (ValueError, UnicodeError):
        raise ScanError("File selection metadata is invalid; no scan was started.") from None
    if not isinstance(metadata, dict) or set(metadata) != {"files", "policy", "lang"}:
        raise ScanError("File selection metadata is invalid; no scan was started.")
    entries, lang = metadata["files"], metadata["lang"]
    if lang not in ("en", "zh") or not isinstance(entries, list) or not 1 <= len(entries) <= Limits().files:
        raise ScanError("Select between 1 and 20 files and a supported language.")
    policy = validate_policy(metadata["policy"])
    offset = length + 4
    inputs = []
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"name", "size"}:
            raise ScanError("File selection metadata is invalid; no scan was started.")
        name, size = entry["name"], entry["size"]
        if not isinstance(name, str) or not 1 <= len(name) <= 255 or any(c in name for c in ("/", "\\", "\x00")):
            raise ScanError("Select named files, not paths or URLs.")
        if type(size) is not int or not 0 <= size <= UPLOAD_BYTES or offset + size > len(body):
            raise ScanError("File snapshot lengths are invalid; no scan was started.")
        inputs.append((safe_path(name), body[offset:offset + size]))
        offset += size
    if offset != len(body) or sum(len(data) for _, data in inputs) > UPLOAD_BYTES:
        raise ScanError("Invalid or oversized selection. Select at most 24 MiB in total.")
    return inputs, policy, lang


class Session:
    def __init__(self):
        self.token = secrets.token_urlsafe(32)
        self.lock = threading.Lock()
        self.reserved = False
        self.closed = False
        self.job = None
        self.last_activity = time.monotonic()
        self.ocr = {"ready": False, "pending": True, "message": "OCR health check has not completed."}

    def health_check(self):
        try:
            ocr = {"ready": True, "pending": False, "message": f"Tesseract {check_ocr()} · English OCR"}
        except ScanError as error:
            ocr = {"ready": False, "pending": False, "message": str(error)}
        with self.lock:
            self.ocr = ocr

    def reserve(self) -> bool:
        with self.lock:
            if self.reserved or self.closed:
                return False
            self.reserved = True
            return True

    def release(self):
        with self.lock:
            self.reserved = False

    def start(self, inputs, policy, lang, *, synthetic=False):
        with self.lock:
            self.job = {"state": "running", "current": 0, "total": len(inputs), "name": "", "synthetic": synthetic}
        threading.Thread(target=self._scan, args=(inputs, policy, lang), daemon=True).start()

    def _scan(self, inputs, policy, lang):
        def progress(current, total, name):
            with self.lock:
                if self.job is not None and not self.closed:
                    self.job.update(current=current, total=total, name=safe_path(name))
        try:
            report = scan_buffers(inputs, policy, progress=progress)
            result = {
                "state": "done", "current": len(inputs), "total": len(inputs), "name": "",
                "high": sum(f.severity == "HIGH" for item in report.files for f in item.findings),
                "warn": sum(f.severity == "WARN" for item in report.files for f in item.findings),
                "incomplete": sum(item.coverage != "inspected" for item in report.files),
                "manual_review": sum(no_readable_text(item) for item in report.files),
                "exit_code": report.exit_code,
                "policy_counts": {"domains": report.domain_count, "cookies": report.cookie_count, "terms": report.term_count},
                "cards": render_cards(report, lang=lang),
            }
        except Exception:
            result = {"state": "error", "message": "Scan could not complete. No privacy decision was made; reselect files and try again."}
        finally:
            # Drop the worker's raw snapshots; keep only masked cards and the
            # explicitly selected normalized visible pixels in the session.
            inputs.clear()
        with self.lock:
            if not self.closed:
                result["synthetic"] = self.job["synthetic"]
                self.job = result
            self.reserved = False

    def status(self):
        with self.lock:
            return dict(self.job) if self.job else {"state": "idle"}

    def clear(self) -> bool:
        with self.lock:
            if self.reserved:
                return False
            self.job = None
            return True

    def close(self):
        with self.lock:
            self.closed = True
            self.job = None
            self.token = ""


class LocalServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = False

    def __init__(self, *, lang="en"):
        if lang not in {"en", "zh"}:
            raise ScanError("GUI language must be en or zh.")
        self.session = Session()
        self.lang = lang
        super().__init__(("127.0.0.1", 0), Handler)
        self.origin = f"http://127.0.0.1:{self.server_port}"
        self.host_header = f"127.0.0.1:{self.server_port}"
        self.timeout = 1

    @property
    def launch_url(self):
        return f"{self.origin}/#{self.session.token}"

    def server_close(self):
        self.session.close()
        super().server_close()


class Handler(BaseHTTPRequestHandler):
    # No access/error logs: headers and paths can contain confidential values.
    def log_message(self, *args):
        pass

    def setup(self):
        super().setup()
        self.connection.settimeout(15)

    def respond(self, code, data, content_type="application/json; charset=utf-8"):
        if isinstance(data, dict):
            data = json.dumps(data, ensure_ascii=True).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", CSP)
        self.send_header("Connection", "close")
        self.end_headers()
        self.close_connection = True
        try:
            self.wfile.write(data)
        except OSError:
            pass

    def permitted(self, *, auth=True):
        # Exact Host validation prevents DNS rebinding. No CORS grants; an
        # unguessable custom header plus Origin checks protect session actions.
        host = self.headers.get_all("Host", [])
        origin = self.headers.get_all("Origin", [])
        if host != [self.server.host_header] or (origin and origin != [self.server.origin]):
            self.respond(403, {"message": "This session accepts requests only from its local page."})
            return False
        if self.headers.get("Sec-Fetch-Site") == "cross-site":
            self.respond(403, {"message": "Cross-site requests are not accepted."})
            return False
        tokens = self.headers.get_all("X-AgentSafe-Session", [])
        token = tokens[0] if len(tokens) == 1 else ""
        expected = self.server.session.token
        if auth and (not expected or not hmac.compare_digest(token.encode("utf-8"), expected.encode("utf-8"))):
            self.respond(401, {"message": "Session expired. Open AgentSafe again to reconnect."})
            return False
        self.server.session.last_activity = time.monotonic()
        return True

    def do_GET(self):
        if not self.permitted(auth=self.path not in ASSETS):
            return
        if self.path in ASSETS:
            name, kind = ASSETS[self.path]
            content = files("agentsafe").joinpath("ui", name).read_bytes()
            if name == "gui.html":
                content = content.replace(b'lang="en"', f'lang="{self.server.lang}"'.encode(), 1)
            self.respond(200, content, kind)
        elif self.path == "/api/info":
            self.respond(200, {"ocr": self.server.session.ocr, "max_files": Limits().files, "max_bytes": UPLOAD_BYTES})
        elif self.path == "/api/status":
            self.respond(200, self.server.session.status())
        else:
            self.respond(404, {"message": "Resource not found."})

    def do_POST(self):
        if not self.permitted():
            return
        session = self.server.session
        if self.path == "/api/clear":
            self.respond(200 if session.clear() else 409, {"message": "Wait for the current scan to finish."})
            return
        if self.path == "/api/stop":
            self.respond(200, {"state": "stopped"})
            session.close()
            return
        if self.path not in {"/api/scan", "/api/demo/before", "/api/demo/after", "/api/demo/miss", "/api/demo/terms"}:
            self.respond(404, {"message": "Resource not found."})
            return
        if not session.reserve():
            self.respond(409, {"message": "Wait for the current scan to finish."})
            return
        try:
            if self.path == "/api/scan":
                sizes = self.headers.get_all("Content-Length", [])
                if len(sizes) != 1 or not sizes[0].isdigit() or self.headers.get("Transfer-Encoding"):
                    raise ScanError("A bounded file selection is required; no scan was started.")
                size = int(sizes[0])
                if not 4 <= size <= UPLOAD_BYTES + HEADER_BYTES + 4 or self.headers.get("Content-Type") != "application/octet-stream":
                    raise ScanError("Invalid or oversized selection. Select at most 24 MiB in total.")
                body = self.rfile.read(size)
                if len(body) != size:
                    raise ScanError("File transfer was incomplete; no scan was started.")
                inputs, policy, lang = decode_upload(body)
            else:
                names = {
                    "/api/demo/before": ["dashboard.png", "session.log"],
                    "/api/demo/after": ["dashboard-reviewed.png", "session-reviewed.log"],
                    "/api/demo/miss": ["small-blurred.png"],
                    "/api/demo/terms": ["business-context.png", "business-context.log"],
                }[self.path]
                assets = files("agentsafe").joinpath("demo_assets")
                inputs = [(name, assets.joinpath(name).read_bytes()) for name in names]
                policy = (Policy(sensitive_terms=("Project Cedar", "Acme Training", "华星演示客户"))
                          if self.path == "/api/demo/terms" else Policy(("northstar.test",), ("demo_session",)))
                lang = self.server.lang
            session.start(inputs, policy, lang, synthetic=self.path != "/api/scan")
            self.respond(202, {"state": "running"})
        except ScanError as error:
            session.release()
            self.respond(400, {"message": str(error)})
        except Exception:
            session.release()
            self.respond(400, {"message": "File selection could not be processed; no scan was started."})


def run_gui(*, lang="en", no_open=False):
    """Open a session; it ends explicitly or after 30 minutes without requests."""
    server = LocalServer(lang=lang)
    threading.Thread(target=server.session.health_check, daemon=True).start()
    try:
        if not no_open and not webbrowser.open(server.launch_url):
            raise ScanError("The browser could not open AgentSafe. Check your default browser and try again.")
        while not server.session.closed and time.monotonic() - server.session.last_activity < IDLE_SECONDS:
            server.handle_request()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
