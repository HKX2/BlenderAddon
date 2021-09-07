using System.Collections.Generic;
using HKX2;

namespace BlenderAddon.Extensions.HKX2
{
    public static partial class Extensions
    {
        public static IEnumerable<BlenderMeshContainer> ToMesh(this hkRootLevelContainerNamedVariant @this)
        {
            var ret = new List<BlenderMeshContainer>();
            ret.AddRange(@this.m_variant.ToMesh());
            return ret;
        }
    }
}