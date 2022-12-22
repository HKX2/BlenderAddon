from typing import Tuple
from enum import Enum

import bpy
from rna_prop_ui import rna_idprop_ui_prop_update


class Materials(Enum):
    Undefined = 0
    Soil = 1
    Stone = 2
    Sand = 3
    Metal = 4
    WireNet = 5
    Grass = 6
    Wood = 7
    Water = 8
    Snow = 9
    Ice = 10
    Lava = 11
    Bog = 12
    HeavySand = 13
    Cloth = 14
    Glass = 15
    Bone = 16
    Rope = 17
    CharControl = 18
    Ragdoll = 19
    Surfing = 20
    GuardianFoot = 21
    HeavySnow = 22
    Unused0 = 23
    LaunchPad = 24
    Conveyer = 25
    Rail = 26
    Grudge = 27
    Meat = 28
    Vegetable = 29
    Bomb = 30
    MagicBall = 31
    Barrier = 32
    AirWall = 33
    Misc = 34
    GrudgeSlow = 35


SUB_MATERIALS = {
    "Barrier": {
        "HolyWall": 1,
    },
    "Bone": {
        "Pile": 1,
    },
    "Cloth": {
        "Carpet": 1,
        "Leather": 2,
    },
    "Grass": {
        "Short": 1,
        "2": 2,
        "WithMud": 3,
        "4": 4,
        "Straw": 5,
        "Thatch": 6,
    },
    "Ice": {
        "1": 1,
        "Hard": 2,
    },
    "Metal": {
        "Light": 1,
    },
    "Sand": {
        "Shallow": 1,
    },
    "Snow": {
        "Shallow": 1,
    },
    "Soil": {
        "Soft": 1,
        "Hard": 2,
    },
    "Stone": {
        "Light": 1,
        "Heavy": 2,
        "Marble": 3,
        "DgnLight": 4,
        "DgnHeavy": 5,
    },
    "Water": {
        "1": 1,
        "2": 2,
        "3": 3,
        "StoneBottom": 4,
    },
    "Wood": {
        "Thin": 1,
        "Thick": 2,
    },
}


class WallCodes(Enum):
    Null = 0
    NoClimb = 1
    Hang = 2
    LadderUp = 3
    Ladder = 4
    Slip = 5
    LadderSide = 6
    NoSlipRain = 7
    NoDashUpAndNoClimb = 8
    IceMakerBlock = 9


class FloorCodes(Enum):
    Null = 0
    Return = 1
    FlowStraight = 2
    FlowLeft = 3
    FlowRight = 4
    Slip = 5
    NarrowPlace = 6
    TopBroadleafTree = 7
    TopConiferousTree = 8
    Fall = 9
    Attach = 10
    NoImpulseUpperMove = 11
    NoPreventFall = 12


class CollisionInfoOperator(bpy.types.Operator):
    bl_idname = "hkx2.collisioninfooperator"
    bl_label = "Change collision info"

    def materials_callback(self, context: bpy.types.Context):
        return tuple((m.name, m.name, "") for m in Materials)

    def sub_materials_callback(self, context: bpy.types.Context):
        material = SUB_MATERIALS.get(self.material)
        sub_materials = (
            (tuple((str(v), k, "") for k, v in material.items())) if material else ()
        )

        return (
            (
                "0",
                "Default",
                "",
            ),
        ) + sub_materials

    def wall_codes_callback(self, context: bpy.types.Context):
        return tuple((w.name, w.name, "") for w in WallCodes)

    def floor_codes_callback(self, context: bpy.types.Context):
        return tuple((f.name, f.name, "") for f in FloorCodes)

    extrafilterik: bpy.props.BoolProperty(
        name="ExtraFilterIK",
        description="",
        default=False,
    )  # type: ignore

    filter_player: bpy.props.BoolProperty(
        name="Player",
        description="",
        default=False,
    )  # type: ignore

    filter_animal: bpy.props.BoolProperty(
        name="Animal",
        description="",
        default=False,
    )  # type: ignore

    filter_npc: bpy.props.BoolProperty(
        name="NPC",
        description="",
        default=False,
    )  # type: ignore

    filter_camera: bpy.props.BoolProperty(
        name="Camera",
        description="",
        default=False,
    )  # type: ignore

    filter_attackhitplayer: bpy.props.BoolProperty(
        name="AttackHitPlayer",
        description="",
        default=False,
    )  # type: ignore

    filter_attackhitenemy: bpy.props.BoolProperty(
        name="AttackHitEnemy",
        description="",
        default=False,
    )  # type: ignore

    filter_arrow: bpy.props.BoolProperty(
        name="Arrow",
        description="",
        default=False,
    )  # type: ignore

    filter_bomb: bpy.props.BoolProperty(
        name="Bomb",
        description="",
        default=False,
    )  # type: ignore

    filter_magnet: bpy.props.BoolProperty(
        name="Magnet",
        description="",
        default=False,
    )  # type: ignore

    filter_camerabody: bpy.props.BoolProperty(
        name="CameraBody",
        description="",
        default=False,
    )  # type: ignore

    filter_ik: bpy.props.BoolProperty(
        name="IK",
        description="",
        default=False,
    )  # type: ignore

    filter_grudge: bpy.props.BoolProperty(
        name="Grudge",
        description="",
        default=False,
    )  # type: ignore

    filter_movingtrolley: bpy.props.BoolProperty(
        name="MovingTrolley",
        description="",
        default=False,
    )  # type: ignore

    filter_lineofsight: bpy.props.BoolProperty(
        name="LineOfSight",
        description="",
        default=False,
    )  # type: ignore

    filter_giant: bpy.props.BoolProperty(
        name="Giant",
        description="",
        default=False,
    )  # type: ignore

    filter_hitall: bpy.props.BoolProperty(
        name="HitAll",
        description="",
        default=False,
    )  # type: ignore

    filter_ignore: bpy.props.BoolProperty(
        name="Ignore",
        description="",
        default=False,
    )  # type: ignore

    material: bpy.props.EnumProperty(
        name="Material",
        description="Material of the object",
        items=materials_callback,
    )  # type: ignore

    sub_material: bpy.props.EnumProperty(
        name="Sub material",
        description="Sub material of the object",
        items=sub_materials_callback,
    )  # type: ignore

    wall_code: bpy.props.EnumProperty(
        name="Wall code",
        description="Wall code of the object",
        items=wall_codes_callback,
    )  # type: ignore

    floor_code: bpy.props.EnumProperty(
        name="Floor code",
        description="Floor code of the object",
        items=floor_codes_callback,
    )  # type: ignore

    collision_filter_info: bpy.props.StringProperty(
        name="",
        description="Hex number representing collision filter info",
    )  # type: ignore

    user_data: bpy.props.StringProperty(
        name="",
        description="Hex number representing user data",
    )  # type: ignore

    def execute(self, context: bpy.types.Context):
        selected_objs = bpy.context.selected_objects
        if not selected_objs:
            self.report({"ERROR"}, "No objects selected")
            return {"CANCELLED"}

        for obj in selected_objs:
            obj["collision_filter_info"] = self.collision_filter_info
            obj["user_data"] = self.user_data
            rna_idprop_ui_prop_update(obj, "collision_filter_info")
            rna_idprop_ui_prop_update(obj, "user_data")

        return {"FINISHED"}

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=800)

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        _row = layout.row()

        col = _row.column()
        box = col.box()

        box.label(text="Collision filter info:")
        box.prop(self, "extrafilterik")
        box.prop(self, "filter_player")
        box.prop(self, "filter_animal")
        box.prop(self, "filter_npc")
        box.prop(self, "filter_camera")
        box.prop(self, "filter_attackhitplayer")
        box.prop(self, "filter_attackhitenemy")
        box.prop(self, "filter_arrow")
        box.prop(self, "filter_bomb")
        box.prop(self, "filter_magnet")
        box.prop(self, "filter_camerabody")
        box.prop(self, "filter_ik")
        box.prop(self, "filter_grudge")
        box.prop(self, "filter_movingtrolley")
        box.prop(self, "filter_lineofsight")
        box.prop(self, "filter_giant")
        box.prop(self, "filter_hitall")
        box.prop(self, "filter_ignore")

        row = box.row()
        row.enabled = False
        row.prop(self, "collision_filter_info")

        col = _row.column()
        box = col.box()

        box.label(text="User data:")
        box.prop(self, "material")
        box.prop(self, "sub_material")
        box.prop(self, "wall_code")
        box.prop(self, "floor_code")

        row = box.row()
        row.enabled = False
        row.prop(self, "user_data")

        material = getattr(Materials, self.material).value
        sub_material = int(self.sub_material)
        wall_code = getattr(WallCodes, self.wall_code).value
        floor_code = getattr(FloorCodes, self.floor_code).value

        collision_filter_info = 0x90000000  # No idea what those leftmost bits mean :(
        collision_filter_info |= self.extrafilterik
        collision_filter_info |= self.filter_player << 8
        collision_filter_info |= self.filter_animal << 9
        collision_filter_info |= self.filter_npc << 10
        collision_filter_info |= self.filter_camera << 11
        collision_filter_info |= self.filter_attackhitplayer << 12
        collision_filter_info |= self.filter_attackhitenemy << 13
        collision_filter_info |= self.filter_arrow << 14
        collision_filter_info |= self.filter_bomb << 15
        collision_filter_info |= self.filter_magnet << 16
        collision_filter_info |= self.filter_camerabody << 17
        collision_filter_info |= self.filter_ik << 18
        collision_filter_info |= self.filter_grudge << 19
        collision_filter_info |= self.filter_movingtrolley << 20
        collision_filter_info |= self.filter_lineofsight << 21
        collision_filter_info |= self.filter_giant << 22
        collision_filter_info |= self.filter_hitall << 23
        collision_filter_info |= self.filter_ignore << 24

        user_data = material
        user_data |= sub_material << 6
        user_data |= floor_code << 10
        user_data |= wall_code << 15

        self.collision_filter_info = f"{collision_filter_info:08X}"
        self.user_data = f"{user_data:08X}"
