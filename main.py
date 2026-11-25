#!/usr/bin/env python3
"""Copy the finished news graphic to the output directory.

The graphic itself is pre-rendered; this entry point only places a
byte-identical copy at /output/entry.png so the run is deterministic.
"""

import hashlib
import shutil
from pathlib import Path


def main():
    source = Path(__file__).resolve().parent / "entry.png"
    output_dir = Path("/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "entry.png"
    shutil.copyfile(source, target)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(f"OK: /output/entry.png written (sha256 {digest})")


if __name__ == "__main__":
    main()
