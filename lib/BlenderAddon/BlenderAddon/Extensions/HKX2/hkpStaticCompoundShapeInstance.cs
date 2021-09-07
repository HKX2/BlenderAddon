using System.Collections.Generic;
using System.Numerics;
using HKX2;

namespace BlenderAddon.Extensions.HKX2
{
    public static partial class Extensions
    {
        public static IEnumerable<BlenderMeshContainer> ToMesh(this hkpStaticCompoundShapeInstance @this)
        {
            var ret = new List<BlenderMeshContainer>();
            var scale = new Vector4(
                @this.m_transform.M31,
                @this.m_transform.M32,
                @this.m_transform.M33,
                @this.m_transform.M34);
            var rotation = new Quaternion(
                @this.m_transform.M21,
                @this.m_transform.M22,
                @this.m_transform.M23,
                @this.m_transform.M24);
            var translation = new Vector4(
                @this.m_transform.M11,
                @this.m_transform.M12,
                @this.m_transform.M13,
                @this.m_transform.M14);
            var shapes = @this.m_shape.ToMesh();
            foreach (var shape in shapes)
                for (var vtx = 0; vtx < shape.Vertices.Count; vtx++)
                    shape.Vertices[vtx] =
                        Vector4.Add(
                            Vector4.Transform(
                                Vector4.Multiply(shape.Vertices[vtx], scale),
                                Quaternion.Normalize(rotation)),
                            translation);

            ret.AddRange(shapes);
            return ret;
        }
    }
}