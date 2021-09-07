using System.Collections.Generic;
using HKX2;

namespace BlenderAddon.Extensions.HKX2
{
    public static partial class Extensions
    {
        public static List<BlenderMeshContainer> ToMesh(this hkpPhysicsData @this)
        {
            var ret = new List<BlenderMeshContainer>();
            foreach (var system in @this.m_systems) ret.AddRange(system.ToMesh());
            return ret;
        }
    }
}