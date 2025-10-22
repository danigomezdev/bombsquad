# ba_meta require api 9
# ba_meta name BombSquadPro
# ba_meta description A mod that unlocks the core features of BombSquad Pro

import babase
import _babase
import _baplus

# ba_meta export babase.Plugin
class byLess(babase.Plugin):
    def mode(test) -> bool:
        return True
    if _babase.env().get("build_number", 0) >= 20884:
        _baplus.get_purchased = mode
