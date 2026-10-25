import socket
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

import pytest

PAGE = b"""<!doctype html>
<html><head><title>Known browser fixture</title></head>
<body><p>Fixture content</p><a href=\"mailto:contact@example.test\">Contact</a></body></html>
"""
EMPTY_PAGE = b""
NOT_FOUND_PAGE = b"<!doctype html><title>Not found fixture</title>"
SERVER_ERROR_PAGE = b"<!doctype html><title>Server error fixture</title>"


class _BrowserTestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        """Return the deterministic response selected by the request path."""
        if self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/contacts")
            self.end_headers()
            return

        responses = {
            "/": (200, PAGE),
            "/contacts": (200, PAGE),
            "/empty": (200, EMPTY_PAGE),
            "/404": (404, NOT_FOUND_PAGE),
            "/500": (500, SERVER_ERROR_PAGE),
        }
        status, body = responses.get(self.path, (404, NOT_FOUND_PAGE))
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        """Suppress server logs during browser tests."""


@pytest.fixture
def local_http_server() -> Iterator[str]:
    """Serve deterministic browser responses on a loopback ephemeral port.

    Yields:
        The server's base URL.
    """
    server = ThreadingHTTPServer(("127.0.0.1", 0), _BrowserTestHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = server.server_address
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


@pytest.fixture
def refused_url() -> str:
    """Return a loopback URL whose port has no listening server."""
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    return f"http://127.0.0.1:{port}/"
