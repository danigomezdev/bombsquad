"""Helper to add a new asset to the bsassets repo and update the cache map.

Usage:
  python3 tools/add_asset.py <file> <platform_dir> <cache_map_path>

Example - adding a new audio file:
  python3 tools/add_asset.py minuevo.ogg common/audio build/assets/lux_data/audio/minuevo.ogg

Example - adding a new DDS texture:
  python3 tools/add_asset.py minuevo.dds desktop/textures build/assets/lux_data/textures/minuevo.dds
"""
import hashlib
import json
import os
import sys
import zlib

CACHE_HEADER = b"efca"


def encode_file(filepath: str) -> tuple[str, bytes]:
    with open(filepath, "rb") as f:
        data = f.read()
    executable = os.access(filepath, os.X_OK)
    meta = ('{"e":true}' if executable else '{"e":false}').encode()
    prefix = CACHE_HEADER + len(meta).to_bytes(1, "big") + meta
    md5 = hashlib.md5()
    md5.update(prefix + data)
    h = md5.hexdigest()
    encoded = prefix + zlib.compress(data)
    return h, encoded


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)

    src_file = sys.argv[1]
    dst_dir = sys.argv[2]  # e.g. "common/audio" or "desktop/textures"
    cache_path = sys.argv[3]  # e.g. "build/assets/lux_data/audio/minuevo.ogg"

    if not os.path.isfile(src_file):
        print(f"ERROR: file not found: {src_file}")
        sys.exit(1)

    h, encoded = encode_file(src_file)

    # Copy to organized directory
    os.makedirs(dst_dir, exist_ok=True)
    dst_file = os.path.join(dst_dir, os.path.basename(src_file))
    with open(dst_file, "wb") as f:
        with open(src_file, "rb") as src:
            f.write(src.read())
    print(f"  Copied: {dst_file}")

    # Store encoded version in hashes/
    hash_dir = os.path.join("hashes", h[:2], h[2:4])
    os.makedirs(hash_dir, exist_ok=True)
    hash_file = os.path.join(hash_dir, h[4:])
    if not os.path.exists(hash_file):
        with open(hash_file, "wb") as f:
            f.write(encoded)
        print(f"  Hashed: hashes/{h[:2]}/{h[2:4]}/{h[4:]}")
    else:
        print(f"  Hash already exists: {h[:12]}...")

    # Update cache map
    cachemap_path = ".lesscachemap"
    with open(cachemap_path) as f:
        cachemap = json.load(f)

    if cache_path in cachemap:
        old_h = cachemap[cache_path]
        if old_h == h:
            print(f"  Cache map unchanged: {cache_path}")
        else:
            print(f"  Cache map updated: {cache_path} ({old_h[:12]}... -> {h[:12]}...)")
    else:
        print(f"  Cache map added: {cache_path}")

    cachemap[cache_path] = h
    with open(cachemap_path, "w") as f:
        json.dump(cachemap, f, indent=2, sort_keys=True)
        f.write("\n")

    print(f"\n  Hash: {h}")
    print(f"  Also add this entry to .lesscachemap in the ballistica repo:")
    print(f'    "{cache_path}": "{h}"')
    print(f"\n  Then: git tag assets-v1.0.N && git push origin assets-v1.0.N")


if __name__ == "__main__":
    main()
