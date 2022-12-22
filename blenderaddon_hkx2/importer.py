from .util import BlenderAddon, System

from pathlib import Path

import bpy
import bmesh


class ImportPackfileOperator(bpy.types.Operator):
    bl_idname = "hkx2.import"
    bl_label = "Import BotW packfile"

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="File path used for importing the Havok file",
        maxlen=1024,
        default="",
        options={"HIDDEN"},
    )  # type: ignore
    files: bpy.props.CollectionProperty(
        type=bpy.types.OperatorFileListElement, options={"HIDDEN"}
    )  # type: ignore
    directory: bpy.props.StringProperty(
        maxlen=1024, default="", subtype="FILE_PATH", options={"HIDDEN"}
    )  # type: ignore
    filter_glob: bpy.props.StringProperty(
        default="*.hkrb;*.hksc;*.hktmrb;*.hknm2", options={"HIDDEN"}
    )  # type: ignore

    transform_teramesh: bpy.props.BoolProperty(
        name="Apply TeraMesh transforms",
        description="Transform TeraMesh (.hktmrb) to match up with StaticCompound (.hksc)",
        default=True,
    )  # type: ignore
    tile_size: bpy.props.FloatProperty(
        name="Tile size",
        description="Size of one TeraMesh segment",
        default=250.0,
        soft_min=10,
        soft_max=1000.0,
    )  # type: ignore
    offset: bpy.props.FloatVectorProperty(
        name="Offset",
        description="Offset for all TeraMesh files",
        default=(-5000.0, 0.0, -4000.0),
        soft_min=-10000.0,
        soft_max=10000.0,
    )  # type: ignore
    use_unsafe_refresh: bpy.props.BoolProperty(
        name='Use "unsafe" viewport refresh',
        description=(
            "Allows using a Blender function to redraw the viewport after every file, "
            "allowing to see some sort of progress indicator"
        ),
        default=True,
    )  # type: ignore

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        wm = bpy.context.window_manager
        wm.fileselect_add(self)

        return {"RUNNING_MODAL"}

    def draw(self, context: bpy.types.Context):
        box = self.layout.box()
        box.prop(self, "transform_teramesh")

        if self.transform_teramesh:
            box.prop(self, "tile_size")
            box.prop(self, "offset")

        box = self.layout.box()
        box.prop(self, "use_unsafe_refresh")

    def execute(self, context: bpy.types.Context):
        for file in self.files:
            file_path = Path(self.directory) / file.name

            # For eventual merging
            added_objects = []

            # Deselect all objects prior to doing anything
            for o in bpy.context.selected_objects:
                o.select_set(False)

            # Parse the meshes
            mesh_containers = BlenderAddon.Converter.Convert(
                str(file_path),
                self.transform_teramesh,
                self.tile_size,
                System.Numerics.Vector3(self.offset[0], self.offset[1], self.offset[2]),
            )

            # Create a bmesh for convex hull creation
            bm = bmesh.new()

            for container in mesh_containers:
                # Construct the blender mesh
                mesh = bpy.data.meshes.new(container.Name)
                obj = bpy.data.objects.new(mesh.name, mesh)
                vertex_group = obj.vertex_groups.new(name=mesh.name)

                # Flip some coordinates to account for BotW coordinate system
                vertices = [(v.X, -v.Z, v.Y) for v in container.Vertices]

                # Import PyData
                mesh.from_pydata(
                    vertices,
                    [],
                    container.Primitives,
                )

                vertex_count = len(vertices)
                vertex_group.add(list(range(vertex_count)), 1.0, "ADD")

                if container.Name in ("hkpConvexVerticesShape", "hkpBoxShape"):
                    bm.from_mesh(mesh)
                    bmesh.ops.convex_hull(bm, input=bm.verts)
                    bm.to_mesh(mesh)
                    mesh.update()
                    bm.clear()

                bpy.context.scene.collection.objects.link(obj)
                added_objects.append(obj)

            if not added_objects:
                self.report({"WARNING"}, "No geometry in this file! (or cannot read!)")
                return {"FINISHED"}

            # Join the objects together
            bpy.context.view_layer.objects.active = added_objects[0]
            [o.select_set(True) for o in added_objects]
            bpy.ops.object.join()
            # Rename the object to match the file
            added_objects[0].name = file_path.stem
            # Remove orphaned meshes
            [
                bpy.data.meshes.remove(m)
                for m in bpy.data.meshes
                if (not m.users) and m.name.startswith("hk")
            ]

            if self.use_unsafe_refresh:
                bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)

        self.report({"INFO"}, "Import finished!")
        return {"FINISHED"}
