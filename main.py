#!/usr/bin/env python3
"""Copy entry.png to the output directory after validating it.

Validation (standard library only): PNG magic bytes, IHDR width/height
of exactly 1024x1024, and a size cap of 1 MiB. The copy is verified
byte-for-byte and its sha256 is printed. Running twice writes identical
bytes because the source image is fixed.
"""
import hashlib
import os
import struct
import sys

MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    target = os.path.join(out_dir, "entry.png")

    try:
        with open(source, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        fail(f"cannot read entry.png: {exc}")

    if len(data) > MAX_BYTES:
        fail(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    if not data.startswith(PNG_MAGIC):
        fail("entry.png does not start with the PNG magic bytes")
    if len(data) < 24 or data[12:16] != b"IHDR":
        fail("entry.png has no IHDR chunk where one belongs")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        fail(f"entry.png is {width}x{height}, expected 1024x1024")

    os.makedirs(out_dir, exist_ok=True)
    with open(target, "wb") as fh:
        fh.write(data)

    with open(target, "rb") as fh:
        written = fh.read()
    if written != data:
        fail("output differs from entry.png byte-for-byte")

    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, {width}x{height})")
    print(f"sha256 {digest}")


if __name__ == "__main__":
    main()
