"""Serve the local preview with byte ranges for video seeking."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
VIDEO = ROOT / "assets" / "video"


class PreviewHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        self.remaining = None
        path = Path(self.translate_path(self.path))
        self.serving_page = path.is_dir() or path.suffix.lower() == ".html"
        if self.serving_page:
            # Always deliver the current HTML during local review.
            del self.headers["If-Modified-Since"]
        requested = self.headers.get("Range")
        if not requested or path.parent != VIDEO or path.suffix != ".mp4" or not path.is_file():
            return super().send_head()

        try:
            video = path.open("rb")
        except OSError:
            return super().send_head()

        size = video.seek(0, 2)
        match = re.fullmatch(r"bytes=(\d*)-(\d*)", requested)
        start = size
        end = size - 1
        if match:
            first, last = match.groups()
            if first:
                start = int(first)
                if last:
                    end = min(end, int(last))
            elif last:
                start = max(0, size - int(last))

        if not 0 <= start <= end:
            video.close()
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return None

        video.seek(start)
        self.remaining = end - start + 1
        self.send_response(206)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(self.remaining))
        self.end_headers()
        return video

    def end_headers(self):
        if getattr(self, "serving_page", False):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def copyfile(self, source, outputfile):
        if self.remaining is None:
            return super().copyfile(source, outputfile)
        while self.remaining > 0:
            chunk = source.read(min(self.remaining, 64 * 1024))
            if not chunk:
                break
            outputfile.write(chunk)
            self.remaining -= len(chunk)


if __name__ == "__main__":
    handler = partial(PreviewHandler, directory=str(ROOT))
    with ThreadingHTTPServer(("127.0.0.1", 5500), handler) as server:
        print("Serving Charlotte’s Pet Podcast at http://localhost:5500/", flush=True)
        server.serve_forever()
