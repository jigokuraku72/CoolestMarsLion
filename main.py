"""The Lion of Mars — coolest-art-01 entry.

Copies the bundled artwork (entry.png) to the competition output
directory and verifies it byte-for-byte.

The grader runs this program in a Docker container where the
MAKEFUN_OUTPUT_DIR environment variable is NOT set; /output is a real
writable mount there, so we fall back to it. Locally, setting
MAKEFUN_OUTPUT_DIR overrides the destination.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"

EXPECTED_SHA256 = "02bd0520103b5156a56ad0a404df00240d4ff6f563eec4b1e3d71e3f87c61123"
EXPECTED_BYTES = 136781
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 683


def jpeg_dimensions(path):
    """Read width/height from a JPEG's SOF marker (stdlib only)."""
    with open(path, "rb") as f:
        data = f.read()
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            height = (data[i + 5] << 8) | data[i + 6]
            width = (data[i + 7] << 8) | data[i + 8]
            return width, height
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seg_len = (data[i + 2] << 8) | data[i + 3]
        i += 2 + seg_len
    raise SystemExit("no JPEG SOF marker found")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def verify(path):
    with open(path, "rb") as f:
        magic = f.read(2)
    if magic != b"\xff\xd8":
        raise SystemExit("not a JPEG: bad magic bytes")
    size = os.path.getsize(path)
    digest = sha256_of(path)
    width, height = jpeg_dimensions(path)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise SystemExit(
            "entry.png dimensions %dx%d, expected %dx%d (uncropped)"
            % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT)
        )
    if size != EXPECTED_BYTES or digest != EXPECTED_SHA256:
        raise SystemExit(
            "entry.png mismatch: size=%d sha256=%s" % (size, digest)
        )
    return size, digest


def main():
    size, digest = verify(SOURCE)
    print("source verified: %d bytes, JPEG magic OK, dimensions %dx%d"
          % (size, EXPECTED_WIDTH, EXPECTED_HEIGHT))
    os.makedirs(OUT_DIR, exist_ok=True)
    dest = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(SOURCE, dest)
    out_size, out_digest = verify(dest)
    print("wrote %s (%d bytes, JPEG magic OK)" % (dest, out_size))
    print("sha256 source=%s" % digest)
    print("sha256 output=%s (match)" % out_digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
