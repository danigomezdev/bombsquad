#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

MODE="${1:-release}"

if [ "$MODE" = "debug" ]; then
    echo "DEBUG mode: using direct import from party/"
    python3 << 'PYEOF'
with open("LessPartyWindow.py", "w", encoding="utf-8") as f:
    f.write("# ba_meta require api 9\n")
    f.write("import party.party\n")
    f.write("from party._updater import UpdateWindow, check_version_blocking\n")
    f.write("import babase\n")
    f.write("# ba_meta export babase.Plugin\n")
    f.write("class byLess(babase.Plugin):\n")
    f.write("    def has_settings_ui(s): return True\n")
    f.write("    def show_settings_ui(s, w): UpdateWindow()  #only_updates\n")
print("LessPartyWindow.py (debug): imports party/ directly")
PYEOF
    echo "Done. Uses mods/party/ directly."

elif [ "$MODE" = "release" ]; then
    echo "RELEASE mode: generating self-extracting bundle"
    python3 << 'PYEOF'
import base64, os, zlib

files = {}
for root, _, filenames in os.walk("party"):
    for fn in filenames:
        if fn.endswith(".pyc"):
            continue
        path = os.path.join(root, fn)
        rel = path
        with open(path, "rb") as f:
            files[rel] = f.read()

with open("LessPartyWindow.py", "w", encoding="utf-8") as out:
    out.write('# ba_meta require api 9\n')
    out.write('import base64 as _b64,os as _os,zlib as _zl,sys as _sys\n')
    out.write('_d=_os.path.dirname(_os.path.abspath(__file__))\n')
    out.write('_r=_os.path.join(_d,"LessPartyWindow")\n')
    out.write('_f={')
    for k, v in sorted(files.items()):
        ek = base64.b64encode(k.encode()).decode()
        ev = base64.b64encode(zlib.compress(v)).decode()
        out.write(f'{ek!r}:{ev!r},')
    out.write('}\n')
    out.write('for _k,_v in _f.items():\n')
    out.write(' _p=_os.path.join(_r,_b64.b64decode(_k).decode())\n')
    out.write(' _os.makedirs(_os.path.dirname(_p),exist_ok=True)\n')
    out.write(' with open(_p,"wb")as _x:_x.write(_zl.decompress(_b64.b64decode(_v)))\n')
    out.write('if _r not in _sys.path:\n')
    out.write(' _sys.path.insert(0,_r)\n')
    out.write('import babase\n')
    out.write('for _m in list(_sys.modules):\n')
    out.write(' if _m=="party" or _m.startswith("party."):\n')
    out.write('  try:del _sys.modules[_m]\n')
    out.write('  except:pass\n')
    out.write('import party.party\n')
    out.write('from party._updater import UpdateWindow, check_version_blocking\n')
    out.write('# ba_meta export babase.Plugin\n')
    out.write('class byLess(babase.Plugin):\n')
    out.write(' def has_settings_ui(s): return True\n')
    out.write(' def show_settings_ui(s, w): UpdateWindow()  #only_updates\n')
    out.write('_me=__file__\n')
    out.write('_light="""# ba_meta require api 9\\n')
    out.write('import sys as _sys,os as _os\\n')
    out.write('_d=_os.path.dirname(_os.path.abspath(__file__))\\n')
    out.write('_r=_os.path.join(_d,"LessPartyWindow")\\n')
    out.write('if _r not in _sys.path:_sys.path.insert(0,_r)\\n')
    out.write('import party.party\\n')
    out.write('from party._updater import UpdateWindow, check_version_blocking\\n')
    out.write('import babase\\n')
    out.write('# ba_meta export babase.Plugin\\n')
    out.write('class byLess(babase.Plugin):\\n')
    out.write(' def has_settings_ui(s): return True\\n')
    out.write(' def show_settings_ui(s, w): UpdateWindow()  #only_updates\\n')
    out.write('"""\n')
    out.write('try:\n')
    out.write(' if _os.path.exists(_os.path.join(_r,"party","__init__.py")):\n')
    out.write('  with open(_me,"w")as _x:_x.write(_light)\n')
    out.write('except:pass\n')

size = os.path.getsize("LessPartyWindow.py")
print(f"LessPartyWindow.py: {size} bytes, {size/1024:.0f} KB")
PYEOF
    echo "Done. Share LessPartyWindow.py."

else
    echo "Usage: $0 [debug|release]"
    echo "  debug   - Uses party/ directly (development)"
    echo "  release - Generates self-extracting bundle (distribution)"
fi
