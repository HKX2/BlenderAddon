from .util import ADDON_DIR

from importlib.util import find_spec

import subprocess
import sys
import os
import bpy

PYTHON_EXECUTABLE = (
    sys.executable if bpy.app.version > (2, 91, 0) else bpy.app.binary_path_python
)

# Ensure Blender's modules directory exists
SITE_DIR = ADDON_DIR.parent.parent / "modules"
SITE_DIR.mkdir(parents=True, exist_ok=True)

# Last confirmed working commit (newer ones might work)
PYTHONNET_COMMIT_HASH = "ec8b69fd35c24efffe39ea3aeb46e373efffb48b"

# URL for `pip install`
PYTHONNET = f"https://github.com/pythonnet/pythonnet/archive/{PYTHONNET_COMMIT_HASH}.zip"


def package_is_installed(package_name: str) -> bool:
    return bool(find_spec(package_name))


def install_package(package: str):
    subprocess.check_call(
        [PYTHON_EXECUTABLE, "-m", "pip", "install", "-t", str(SITE_DIR), package]
    )


class DependenciesOperator(bpy.types.Operator):
    bl_idname = "hkx2.dependenciesoperator"
    bl_label = "Install dependencies"

    def execute(self, context: bpy.types.Context):
        install_package(PYTHONNET)

        os.execvp(sys.argv[0], sys.argv)
