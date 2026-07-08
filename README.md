# Bombsquad Assets

Prebuilt game assets for the Ballistica project. Files are content-addressed by MD5 hash and served via GitHub raw content. The ballistica project downloads them via `lesscache_repository_url`.

Note: this repo tracks its own asset index in `.lesscachemap` (path -> MD5 hash
of the files stored under `hashes/`). The ballistica repo has a separate file
with the same name that maps project build paths to the same hashes. Both
files share a name but live in different repos and are not the same file.

## Structure

```
common/         audio (.ogg), fonts (.fdata), data (.json), meshes (.bob/.cob), python
desktop/        textures (.dds) for Linux, macOS, Windows
mobile/         textures (.ktx) for Android and iOS
android/        Python stdlib + native .a libraries
ios/            Python.xcframework (BeeWare)
windows/        DLLs, debug Python, ANGLE
previews/       PNG texture previews (all platforms)
hashes/         All files encoded with lesscache format, named by MD5 hash
```

## How it works

Lesscache stores files content-addressed by MD5 hash in the `hashes/` directory. The URL scheme is:

```
https://raw.githubusercontent.com/danigomezdev/bombsquad/assets/hashes/<aa>/<bb>/<rest>
```

Where `<aa><bb><rest>` is the MD5 hash of the original file. The stored file is wrapped in the lesscache format:

```
+------+-------+----------+-------------------+
| efca | metalen| metadata | zlib-compressed   |
| 4 B  | 1 B    | N B      | original content  |
+------+-------+----------+-------------------+
```

The `metadata` JSON contains `{"e": false}` (e=executable flag).

On the ballistica side, `.lesscachemap` maps project paths to MD5 hashes:

```json
{
  "build/assets/windows/x64/discord_partner_sdk.dll": "5c8d0dda1045115b5b019eeefad10d5f",
  "build/assets/lux_data/textures/white.dds": "a1b2c3d4..."
}
```

When building, the CI downloads from lesscache, decompresses, and stages the file at its project path.

## Adding a new asset

### 1. Place the file in its project location

```bash
cp myfile.dll /path/to/ballistica/build/assets/windows/x64/
```

### 2. Encode with lesscache format

```python
import json, zlib

with open('/path/to/build/assets/windows/x64/myfile.dll', 'rb') as f:
    raw = f.read()

# Compute MD5 of original content
import hashlib
hashval = hashlib.md5(raw).hexdigest()

# Prepare metadata
meta = b'{"e":false}'

# Build cache file
cache = b'efca' + bytes([len(meta)]) + meta + zlib.compress(raw, 9)

# Write to hashes directory using MD5 path scheme
import os
prefix = hashval[:2]
subdir = hashval[2:4]
rest = hashval[4:]
os.makedirs(f'hashes/{prefix}/{subdir}', exist_ok=True)
with open(f'hashes/{prefix}/{subdir}/{rest}', 'wb') as f:
    f.write(cache)

print(f'hash: {hashval}')
print(f'path: hashes/{prefix}/{subdir}/{rest}')
```

### 3. Commit and push to this repo

```bash
git add hashes/ && git commit -m "add myfile.dll"
git push origin assets
```

### 4. Add to .lesscachemap in the ballistica project

```bash
cd /path/to/ballistica
python3 -c "
import json
with open('.lesscachemap') as f:
    m = json.load(f)
m['build/assets/windows/x64/myfile.dll'] = 'HASH_VALUE_HERE'
m = dict(sorted(m.items()))
with open('.lesscachemap', 'w') as f:
    json.dump(m, f, indent=2)
"
git add .lesscachemap && git commit -m "add myfile.dll to lesscachemap"
```

### 5. Wait for CDN propagation

`raw.githubusercontent.com` caches content for 300 seconds. Wait at least 5 minutes after pushing before triggering a CI build.

### 6. Verify

```bash
cd /path/to/ballistica
python3 -c "
import sys; sys.path.insert(0, 'tools')
from lesstools.lesscache import get_target
get_target('build/assets/windows/x64/myfile.dll', batch=False)
print('OK')
"
```

## Platform directory reference

| Directory | Format | Used by |
|-----------|--------|---------|
| `common/audio/` | `.ogg` | All |
| `common/fonts/` | `.fdata` | All |
| `common/data/` | `.json` | All |
| `common/meshes/` | `.bob`, `.cob` | All |
| `common/python/` | `.py` | All |
| `desktop/textures/` | `.dds` | Linux, macOS, Windows |
| `mobile/textures/` | `.ktx` | Android, iOS |
| `previews/textures/` | `.png` | All |
| `android/pylib/` | `.py` | Android |
| `android/native/` | `.a` | Android |
| `ios/` | `.xcframework` | iOS |
| `windows/extras/` | `.dll`, `.pyd` | Windows |

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Invalid cache header` | File uploaded raw instead of lesscache-wrapped | Re-encode with `efca` header and re-upload |
| `Path not found in lesscache` | Entry missing from `.lesscachemap` in ballistica repo | Add the path→hash mapping |
| `Download failed` | Network or CDN propagation delay | Wait 5 min and retry |
| `HTTP 404` | File not yet pushed to `assets` branch | Push to `origin assets` |
