from pathlib import Path

import sys


ADDON_DIR = Path(__file__).parent


def initialize_libs():
    lib_dir = ADDON_DIR / "lib"

    from clr_loader import get_coreclr
    from pythonnet import set_runtime

    rt = get_coreclr(str(lib_dir / "net5.0.runtimeconfig.json"))
    set_runtime(rt)

    sys.path.insert(0, str(lib_dir))

    import clr

    clr.AddReference("HKX2")
    clr.AddReference("HKX2Builders")
    clr.AddReference("BlenderAddon")
    clr.AddReference("System")

    import HKX2
    import HKX2Builders
    import BlenderAddon
    import System

    globals().update(
        {
            "HKX2": HKX2,
            "HKX2Builders": HKX2Builders,
            "BlenderAddon": BlenderAddon,
            "System": System,
        }
    )
