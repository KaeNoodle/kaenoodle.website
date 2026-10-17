# serve.py: local preview server for kaenoodle.au
#
# Python's built-in server (python -m http.server) can't handle clean
# URLs like /projects, because Azure rewrites extensionless URLs using
# staticwebapp.config.json, which the built-in server ignores.
#
# This subclass adds that one behaviour: if the requested path has no
# file, try the same path with .html on the end. That makes local links
# behave the same way they will in production, so a broken link shows up
# here instead of after deploying.
#
# Run it with:  python serve.py
# Then open:    http://localhost:8000

import functools
import http.server
import socketserver
from pathlib import Path

PORT = 8000
ROOT = Path(__file__).parent


class CleanURLHandler(http.server.SimpleHTTPRequestHandler):

    def translate_path(self, path):
        # Let the parent class do the real work: strip the query string,
        # decode escapes, and block paths that try to climb out of the
        # served directory.
        resolved = Path(super().translate_path(path))

        # A real file or a directory with an index: nothing to do.
        if resolved.is_file():
            return str(resolved)
        if resolved.is_dir() and (resolved / "index.html").is_file():
            return str(resolved)

        # Otherwise try the .html version, which is the rewrite Azure
        # performs from staticwebapp.config.json.
        with_html = resolved.with_suffix(".html")
        if with_html.is_file():
            return str(with_html)

        # Nothing matched. Hand back the original so the parent class
        # returns a normal 404 rather than something misleading.
        return str(resolved)

    def log_message(self, fmt, *args):
        # Quieter than the default, which prints the date on every line.
        print(f"  {fmt % args}")


def main():
    handler = functools.partial(CleanURLHandler, directory=str(ROOT))

    # allow_reuse_address stops "address already in use" when you stop
    # and restart the server quickly.
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
        print(f"Serving {ROOT.name} at http://localhost:{PORT}")
        print("Ctrl+C to stop.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
