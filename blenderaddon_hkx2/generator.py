from .util import BlenderAddon, HKX2Builders, HKX2, System

from pathlib import Path

import bpy
import bpy_extras
import bmesh


class GeneratorOperator(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "hkx2.generate"
    bl_label = "Generate BotW packfile"

    filename_ext = ""

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="File path used for importing the Havok file",
        maxlen=1024,
        default="",
        options={"HIDDEN"},
    )  # type: ignore
    filter_glob: bpy.props.StringProperty(
        default="*.hkrb;*.hksc;*.hktmrb;*.hknm2",
        options={"HIDDEN"})  # type: ignore

    selected_objects_only: bpy.props.BoolProperty(
        name="Selected objects only",
        description="Use only selected objects for generation",
        default=False,
    )  # type: ignore

    platform: bpy.props.EnumProperty(
        name="Platform",
        description="Choose which platform header to use for generating",
        items=(
            ("wiiu", "Wii U", ""),
            ("nx", "Switch", ""),
        ),  # type: ignore
        default="wiiu",  # type: ignore
    )  # type: ignore
    havok_type: bpy.props.EnumProperty(
        name="Havok type",
        description="Choose which type of file to generate",
        items=(
            (".hkrb", "Havok Rigid Body (*.hkrb)", ""),
            (".hksc", "Havok Static Compound (*.hksc)", ""),
            (".hktmrb", "Havok Tera Mesh Rigid Body (*.hktmrb)", ""),
            (".hknm2", "Havok Navigation Mesh (*.hknm2)", ""),
        ),  # type: ignore
        default=".hkrb",  # type: ignore
    )  # type: ignore

    use_custom_collision_info: bpy.props.BoolProperty(
        name="Use custom collision info",
        description=
        "If provided in object properties, use custom collision info",
        default=True,
    )  # type: ignore

    cell_size: bpy.props.FloatProperty(
        name="Cell size",
        default=0.3,
    )  # type: ignore
    cell_height: bpy.props.FloatProperty(
        name="Cell height",
        default=0.3,
    )  # type: ignore
    walkable_slope_angle: bpy.props.FloatProperty(
        name="Walkable slope angle",
        default=30.0,
    )  # type: ignore
    walkable_height: bpy.props.FloatProperty(
        name="Walkable height",
        default=2.0,
    )  # type: ignore
    walkable_climb: bpy.props.FloatProperty(
        name="Walkable climb",
        default=1.0,
    )  # type: ignore
    walkable_radius: bpy.props.FloatProperty(
        name="Walkable radius",
        default=0.5,
    )  # type: ignore
    min_region_area: bpy.props.IntProperty(
        name="Min region area",
        default=3,
    )  # type: ignore

    # Borrowed from glTF addon
    def on_havok_type_change(self, context: bpy.types.Context):
        sfile = context.space_data

        if not isinstance(sfile, bpy.types.SpaceFileBrowser):
            return

        if not sfile.active_operator:
            return

        if sfile.active_operator.bl_idname != "HKX2_OT_generate":
            return

        sfile.params.filename = str(
            Path(sfile.params.filename).with_suffix(self.havok_type))

    def draw(self, context: bpy.types.Context):
        self.on_havok_type_change(context)

        box = self.layout.box()
        box.prop(self, "selected_objects_only")  # type: ignore

        box = self.layout.box()
        box.prop(self, "platform", text="")  # type: ignore
        box.prop(self, "havok_type", text="")  # type: ignore

        if self.havok_type in (".hkrb", ".hktmrb", ".hksc"):
            box.prop(self, "use_custom_collision_info")  # type: ignore

        if self.havok_type == ".hknm2":
            box.prop(self, "cell_size")  # type: ignore
            box.prop(self, "cell_height")  # type: ignore
            box.prop(self, "walkable_slope_angle")  # type: ignore
            box.prop(self, "walkable_height")  # type: ignore
            box.prop(self, "walkable_climb")  # type: ignore
            box.prop(self, "walkable_radius")  # type: ignore
            box.prop(self, "min_region_area")  # type: ignore

    def execute(self, context: bpy.types.Context):
        vertices = System.Collections.Generic.List[System.Numerics.Vector3]()
        indices = System.Collections.Generic.List[System.UInt32]()
        collision_info = System.Collections.Generic.List[System.Tuple[
            System.UInt32, System.UInt32]]()

        objects_to_iter = [
            o for o in (bpy.context.selected_objects if self.
                        selected_objects_only else bpy.data.objects)
            if o.type == "MESH"
        ]

        if not objects_to_iter:
            self.report(
                {"ERROR"},
                f"No objects {'selected' if self.selected_objects_only else 'exist'}!",
            )
            return {"CANCELLED"}

        bm = bmesh.new()

        for obj in objects_to_iter:
            dg = bpy.context.evaluated_depsgraph_get()
            obj = obj.evaluated_get(dg)
            me = obj.to_mesh()

            bm.from_mesh(me)

            # Coincidentally happens to not take effect on the original mesh
            bmesh.ops.triangulate(bm, faces=bm.faces[:])

            vert_length = len(vertices)

            for vtx in me.vertices:
                vec = obj.matrix_world @ vtx.co
                vertices.Add(System.Numerics.Vector3(vec.x, vec.z, -vec.y))

            for face in bm.faces:
                [indices.Add(vert_length + vtx.index) for vtx in face.verts]

            collision_filter_info = 0x90000000
            user_data = 0x00000002

            if self.use_custom_collision_info:
                collision_filter_info_string = obj.get("collision_filter_info")
                user_data_string = obj.get("user_data")

                if collision_filter_info_string:
                    collision_filter_info = int(collision_filter_info_string,
                                                base=16)

                if user_data_string:
                    user_data = int(user_data_string, base=16)

            [
                collision_info.Add(System.Tuple[System.UInt32, System.UInt32](
                    collision_filter_info, user_data)) for _ in bm.faces
            ]

            bm.clear()

        header = None
        if self.platform == "wiiu":
            header = HKX2.HKXHeader.BotwWiiu()
        elif self.platform == "nx":
            header = HKX2.HKXHeader.BotwNx()

        try:
            if self.havok_type == ".hkrb":
                BlenderAddon.Generator.GenerateHkrb(self.filepath, header,
                                                    vertices, indices,
                                                    collision_info)
            elif self.havok_type == ".hktmrb":
                BlenderAddon.Generator.GenerateHktmrb(self.filepath, header,
                                                      vertices, indices,
                                                      collision_info)
            elif self.havok_type == ".hksc":
                BlenderAddon.Generator.GenerateHksc(self.filepath, header,
                                                    vertices, indices,
                                                    collision_info)
            elif self.havok_type == ".hknm2":
                config = HKX2Builders.hkaiNavMeshBuilder.Config.Default()

                config.CellSize = self.cell_size
                config.CellHeight = self.cell_height
                config.WalkableSlopeAngle = self.walkable_slope_angle
                config.WalkableHeight = self.walkable_height
                config.WalkableClimb = self.walkable_climb
                config.WalkableRadius = self.walkable_radius
                config.MinRegionArea = self.min_region_area

                BlenderAddon.Generator.GenerateHknm2(self.filepath, header,
                                                     vertices, indices, config)
        except Exception as e:
            self.report({"ERROR"}, f"{type(e).__name__}: {e}")
            return {"CANCELLED"}

        self.report({"INFO"}, "Export finished!")
        return {"FINISHED"}
