#!/usr/bin/env python3
"""Copy the pre-rendered entry.png to $MAKEFUN_OUTPUT_DIR/entry.png.

Pure standard library. Nothing is rendered here: the judging machine has
no font library, so the page is rendered in advance by tools/gen_image.py
and shipped as entry.png next to this file. This script only validates
the PNG and copies it.
"""
import hashlib
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(1)


def check_png(data):
    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("entry.png does not start with the PNG magic bytes")
    pos = 8
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated PNG chunk header")
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(data):
            fail("truncated PNG chunk %r" % ctype)
        stored = struct.unpack(">I", data[end - 4:end])[0]
        actual = zlib.crc32(data[pos + 4:end - 4]) & 0xFFFFFFFF
        if stored != actual:
            fail("CRC mismatch in PNG chunk %r" % ctype)
        pos = end
        if ctype == b"IEND":
            break
    else:
        fail("no IEND chunk found in entry.png")
    if pos != len(data):
        fail("trailing data after IEND chunk (%d extra bytes)" % (len(data) - pos))
    if data[12:16] != b"IHDR":
        fail("first PNG chunk is not IHDR")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        fail("entry.png is %dx%d, expected 1024x1024" % (width, height))
    if data[25] != 2:
        fail("entry.png colour type is %d, expected 2 (RGB)" % data[25])


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    with open(SRC, "rb") as f:
        data = f.read()
    check_png(data)
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (dst, len(data)))
    print("sha256 %s" % hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
