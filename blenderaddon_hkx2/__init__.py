bl_info = {
    "name": "HKX2 Integration",
    "author": "kreny",
    "description": "Blender addon to accompany HKX2 library.",
    "blender": (2, 93, 0),
    "version": (1, 0, 0),
}


from .util import initialize_libs
from .dependencies import package_is_installed

import bpy


PYTHONNET_INSTALLED = package_is_installed("pythonnet")

if PYTHONNET_INSTALLED:
    initialize_libs()

from .collision_info import CollisionInfoOperator
from .dependencies import DependenciesOperator

try:
    from .importer import ImportPackfileOperator
    from .generator import GeneratorOperator
except ImportError:
    PYTHONNET_INSTALLED = False


OPERATORS = tuple(
    globals()[key]
    for key in globals().keys()
    if ("Operator" in key) and (key != "DependenciesOperator")
)


class HKX2Panel(bpy.types.Panel):
    bl_idname = "HKX2_PT_panel"
    bl_category = "HKX2"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_label = "HKX2"

    def draw(self, context: bpy.types.Context):
        if not PYTHONNET_INSTALLED:
            self.layout.operator(DependenciesOperator.bl_idname)
            return

        for operator in OPERATORS:
            self.layout.operator(operator.bl_idname)


classes = (HKX2Panel, DependenciesOperator, *OPERATORS)

reg, unreg = bpy.utils.register_classes_factory(classes)


def register():
    reg()


def unregister():
    unreg()
