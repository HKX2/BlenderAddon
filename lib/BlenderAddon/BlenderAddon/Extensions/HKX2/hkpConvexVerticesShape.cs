using System.Collections.Generic;
using System.Numerics;
using HKX2;

namespace BlenderAddon.Extensions.HKX2
{
    public static partial class Extensions
    {
        public static List<BlenderMeshContainer> ToMesh(this hkpConvexVerticesShape @this)
        {
            var cont = new BlenderMeshContainer(@this.GetType().Name);
            foreach (var rV in @this.m_rotatedVertices)
            {
                cont.Vertices.Add(new Vector4(rV.M11, rV.M21, rV.M31, 1f));
                cont.Vertices.Add(new Vector4(rV.M12, rV.M22, rV.M32, 1f));
                cont.Vertices.Add(new Vector4(rV.M13, rV.M23, rV.M33, 1f));
                cont.Vertices.Add(new Vector4(rV.M14, rV.M24, rV.M34, 1f));
            }

            return new List<BlenderMeshContainer> {cont};
        }
    }
}