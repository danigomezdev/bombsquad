# To learn more, see https://ballistica.net/wiki/meta-tag-system
# ba_meta require api 9

import babase
import _babase
import _baplus

# ba_meta export plugin
class BSPro(babase.Plugin):
    def mode(test) -> bool:
        return True
    if _babase.env().get("build_number", 0) >= 20884:
        _baplus.get_purchased = mode
