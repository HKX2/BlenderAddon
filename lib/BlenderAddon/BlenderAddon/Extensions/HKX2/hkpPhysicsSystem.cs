using System.Collections.Generic;
using HKX2;

namespace BlenderAddon.Extensions.HKX2
{
    public static partial class Extensions
    {
        public static IEnumerable<BlenderMeshContainer> ToMesh(this hkpPhysicsSystem @this)
        {
            var ret = new List<BlenderMeshContainer>();
            foreach (var rigidBody in @this.m_rigidBodies) ret.AddRange(rigidBody.ToMesh());
            return ret;
        }
    }
}