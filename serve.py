"""Static file server with SPA fallback: unknown paths serve index.html
so client-side routing (pushState) works on refresh and deep links."""
import http.server
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8732
ROOT = os.path.dirname(os.path.abspath(__file__))


class SPAHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        fs_path = os.path.join(ROOT, path.lstrip("/"))
        if path != "/" and not os.path.isfile(fs_path):
            self.path = "/index.html"
        return super().do_GET()


if __name__ == "__main__":
    with http.server.ThreadingHTTPServer(("", PORT), SPAHandler) as httpd:
        httpd.serve_forever()
