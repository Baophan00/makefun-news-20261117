#!/usr/bin/env python3
"""Copy the poster to /output and verify the copy is byte-identical.

Standard library only. No network, randomness, or timestamps.
"""

from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
DEST_DIR = Path("/output")
DEST = DEST_DIR / "entry.png"


def main():
    data = SOURCE.read_bytes()
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    DEST.write_bytes(data)
    if DEST.read_bytes() != data:
        raise SystemExit("verification failed: /output/entry.png differs from entry.png")
    print(f"entry.png {len(data)} bytes")


if __name__ == "__main__":
    main()
