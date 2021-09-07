using System.Collections.Generic;
using System.Linq;
using HKX2;

namespace BlenderAddon.Extensions.HKX2
{
    public static partial class Extensions
    {
        public static List<BlenderMeshContainer> ToMesh(this hkRootLevelContainer @this)
        {
            var ret = new List<BlenderMeshContainer>();
            foreach (var namedVariant in @this.m_namedVariants) ret.AddRange(namedVariant.ToMesh());

            return ret;
        }

        public static T FindVariant<T>(this hkRootLevelContainer @this) where T : hkReferencedObject
        {
            return (from v in @this.m_namedVariants where v.m_className == typeof(T).Name select (T) v.m_variant)
                .FirstOrDefault();
        }
    }
}