using System.Collections.Generic;
using HKX2;

namespace BlenderAddon.Extensions.HKX2
{
    public static partial class Extensions
    {
        public static List<BlenderMeshContainer> ToMesh(this hkpStaticCompoundShape @this)
        {
            var ret = new List<BlenderMeshContainer>();
            foreach (var instance in @this.m_instances) ret.AddRange(instance.ToMesh());
            return ret;
        }
    }
}