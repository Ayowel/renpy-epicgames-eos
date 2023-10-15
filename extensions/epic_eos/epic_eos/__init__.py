
__version__ = '0.2.2'
__eos_version__ = '1.15.4'

eos_platform = None # type: epic_eos.cdefs.EOS_HPlatform
renpy_category = 'LogEOSRenpy'

import epic_eos.cdefs
import epic_eos.compat
import epic_eos.ren

from .compat import (epic_init, epic_shutdown)
from .ren import (is_epic_available)
