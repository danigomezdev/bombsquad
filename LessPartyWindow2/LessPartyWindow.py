# ba_meta require api 9
# ba_meta require asset-package 581
import sys as _sys,os as _os
_d=_os.path.dirname(_os.path.abspath(__file__))
_r=_os.path.join(_d,"LessPartyWindow")
if _r not in _sys.path:_sys.path.insert(0,_r)
import party.party
from party._updater import UpdateWindow, check_version_blocking
import babase
# ba_meta export babase.Plugin
class byLess(babase.Plugin):
 def has_settings_ui(s): return True
 def show_settings_ui(s, w): UpdateWindow()  #only_updates
