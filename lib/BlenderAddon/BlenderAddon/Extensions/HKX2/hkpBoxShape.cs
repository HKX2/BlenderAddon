using System.Collections.Generic;
using System.Numerics;
using HKX2;

namespace BlenderAddon.Extensions.HKX2
{
    public static partial class Extensions
    {
        public static List<BlenderMeshContainer> ToMesh(this hkpBoxShape @this)
        {
            var cont = new BlenderMeshContainer(@this.GetType().Name);
            var hE = @this.m_halfExtents;
            var bbMin = new Vector4(0f - hE.X, 0f - hE.Y, 0f - hE.Z, 1f);
            var bbMax = new Vector4(hE.X, hE.Y, hE.Z, 1f);
            cont.Vertices.AddRange(new List<Vector4>
            {
                bbMin,
                bbMax,
                new(bbMin.X, bbMin.Y, bbMax.Z, 1f),
                new(bbMin.X, bbMax.Y, bbMin.Z, 1f),
                new(bbMax.X, bbMin.Y, bbMin.Z, 1f),
                new(bbMin.X, bbMax.Y, bbMax.Z, 1f),
                new(bbMax.X, bbMin.Y, bbMax.Z, 1f),
                new(bbMax.X, bbMax.Y, bbMin.Z, 1f)
            });
            return new List<BlenderMeshContainer> {cont};
        }
    }
}