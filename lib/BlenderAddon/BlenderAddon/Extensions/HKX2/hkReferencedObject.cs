using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using HKX2;

namespace BlenderAddon.Extensions.HKX2
{
    public static partial class Extensions
    {
        private static readonly List<string> ExcludedClasses = new();

        public static List<BlenderMeshContainer> ToMesh(this hkReferencedObject @this)
        {
            var extensions = typeof(Extensions);
            var type = @this.GetType();
            var methodToMesh = extensions
                .GetMethods(BindingFlags.Public | BindingFlags.Static).FirstOrDefault(m =>
                    m.Name == "ToMesh" && m.GetParameters().First().ParameterType == type);

            if (methodToMesh != null && type.Name != nameof(hkReferencedObject))
                return (List<BlenderMeshContainer>) methodToMesh.Invoke(null, new[] {@this});

            if (ExcludedClasses.Contains(@this.GetType().Name)) return new List<BlenderMeshContainer>();

            Console.Error.WriteLine("'" + @this.GetType().Name + "' not implemented, ignoring");
            ExcludedClasses.Add(@this.GetType().Name);
            return new List<BlenderMeshContainer>();
        }
    }
}