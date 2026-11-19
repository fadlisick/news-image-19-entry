"""Place the finished poster where the grader reads it.

The poster itself is drawn by draw_poster.py; this entrypoint only
validates it and copies it into the output directory. Standard
library only, so it runs unchanged in the grader's offline
container, on any Python 3.
"""

import hashlib
import os
import shutil
import sys

MAX_BYTES = 1024 * 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def poster_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.png")


def check_poster(path):
    with open(path, "rb") as handle:
        magic = handle.read(len(PNG_MAGIC))
    if magic != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG file")
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit("entry.png is over the 1 MiB limit")
    return size


def main(argv=None):
    src = poster_path()
    size = check_poster(src)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    digest = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    print("wrote %s (%d bytes, sha256 %s)" % (dst, size, digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
