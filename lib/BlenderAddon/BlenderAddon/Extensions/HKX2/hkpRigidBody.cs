using System.Collections.Generic;
using HKX2;

namespace BlenderAddon.Extensions.HKX2
{
    public static partial class Extensions
    {
        public static IEnumerable<BlenderMeshContainer> ToMesh(this hkpRigidBody @this)
        {
            return ToMesh((hkpEntity) @this);
        }
    }
}