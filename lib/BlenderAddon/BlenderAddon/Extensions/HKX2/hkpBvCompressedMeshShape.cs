using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using HKX2;

namespace BlenderAddon.Extensions.HKX2
{
    public static partial class Extensions
    {
        public static List<BlenderMeshContainer> ToMesh(this hkpBvCompressedMeshShape @this)
        {
            var sections = new List<Section>();
            var domain = new Domain(@this.m_tree.m_domain.m_min, @this.m_tree.m_domain.m_max);
            var sharedVerts = @this.m_tree.m_sharedVertices.Select(vtx2 => new SharedVertex(vtx2).Decompress(domain))
                .ToList();

            foreach (var sec in @this.m_tree.m_sections)
            {
                var s = new Section
                {
                    Domain = new Domain(sec.m_domain.m_min, sec.m_domain.m_max),
                    Vertices = new List<Vector4>(),
                    Primitives = new List<List<byte>>()
                };
                sections.Add(s);
                var offset = new Vector3(sec.m_codecParms_0, sec.m_codecParms_1, sec.m_codecParms_2);
                var scale = new Vector3(sec.m_codecParms_3, sec.m_codecParms_4, sec.m_codecParms_5);
                var sharedVtxIndexStart = sec.m_sharedVertices.m_data >> 8;
                var primitiveStart = sec.m_primitives.m_data >> 8;
                var primitiveCount = sec.m_primitives.m_data & 0xFFu;
                foreach (var vtx in new ArraySegment<uint>(@this.m_tree.m_packedVertices.ToArray(),
                    (int) sec.m_firstPackedVertex, sec.m_numPackedVertices))
                    s.Vertices.Add(new PackedVertex(vtx).Decompress(offset, scale));

                foreach (var idx in new ArraySegment<ushort>(@this.m_tree.m_sharedVerticesIndex.ToArray(),
                    (int) sharedVtxIndexStart, sec.m_numSharedIndices))
                    s.Vertices.Add(sharedVerts[idx]);

                foreach (var primitive2 in new
                    ArraySegment<hkcdStaticMeshTreeBasePrimitive>(@this.m_tree.m_primitives.ToArray(),
                        (int) primitiveStart,
                        (int) primitiveCount))
                    s.Primitives.Add(new List<byte>
                    {
                        primitive2.m_indices_0, primitive2.m_indices_1, primitive2.m_indices_2, primitive2.m_indices_3
                    });
            }

            var cont = new BlenderMeshContainer(@this.GetType().Name);
            var vtxCount = 0;
            foreach (var sec in sections)
            {
                cont.Vertices.AddRange(sec.Vertices);
                var primitives = sec.Primitives.Select(primitive => new List<int>
                {
                    primitive[0] + vtxCount, primitive[1] + vtxCount, primitive[2] + vtxCount, primitive[3] + vtxCount
                }).ToList();

                cont.Primitives.AddRange(primitives);
                vtxCount += sec.Vertices.Count;
            }

            return new List<BlenderMeshContainer> {cont};
        }
    }
}