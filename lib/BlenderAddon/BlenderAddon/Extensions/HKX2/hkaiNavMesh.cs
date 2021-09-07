using System;
using System.Collections.Generic;
using System.Linq;
using HKX2;

namespace BlenderAddon.Extensions.HKX2
{
    public static partial class Extensions
    {
        public static List<BlenderMeshContainer> ToMesh(this hkaiNavMesh @this)
        {
            var cont = new BlenderMeshContainer(@this.GetType().Name)
            {
                Vertices = @this.m_vertices
            };

            foreach (var face in @this.m_faces)
            {
                var faceEdgeVerticesFlattened = new List<int>();
                for (var i = face.m_startEdgeIndex; i < face.m_startEdgeIndex + face.m_numEdges; i++)
                {
                    faceEdgeVerticesFlattened.Add(@this.m_edges[i].m_a);
                    faceEdgeVerticesFlattened.Add(@this.m_edges[i].m_b);
                }
                cont.Primitives.Add(faceEdgeVerticesFlattened.Distinct().ToList());
            }

            return new List<BlenderMeshContainer> {cont};
        }
    }
}