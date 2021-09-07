using System.Collections.Generic;
using HKX2;

namespace BlenderAddon.Extensions.HKX2
{
    public static partial class Extensions
    {
        public static IEnumerable<BlenderMeshContainer> ToMesh(this hkpListShape @this)
        {
            var ret = new List<BlenderMeshContainer>();
            foreach (var childInfo in @this.m_childInfo) ret.AddRange(childInfo.ToMesh());

            return ret;
        }
    }
}