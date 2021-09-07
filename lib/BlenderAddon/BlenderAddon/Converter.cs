using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Numerics;
using BlenderAddon.Extensions.HKX2;
using HKX2;

namespace BlenderAddon
{
    public class Domain
    {
        public Vector4 Max;
        public Vector4 Min;

        public Domain(Vector4 min, Vector4 max)
        {
            Min = min;
            Max = max;
        }
    }

    public class Section
    {
        public Domain Domain;

        public List<List<byte>> Primitives;

        public List<Vector4> Vertices;
    }

    public class PackedVertex
    {
        private readonly uint _vtx;

        public PackedVertex(uint vtx)
        {
            _vtx = vtx;
        }

        public Vector4 Decompress(Vector3 offset, Vector3 scale)
        {
            return new Vector4((_vtx & 0x7FFu) * scale.X + offset.X,
                ((_vtx >> 11) & 0x7FFu) * scale.Y + offset.Y,
                ((_vtx >> 22) & 0x3FFu) * scale.Z + offset.Z, 1f);
        }
    }

    public class SharedVertex
    {
        private readonly ulong _vtx;

        public SharedVertex(ulong vtx)
        {
            _vtx = vtx;
        }

        public Vector4 Decompress(Domain domain)
        {
            var offset = domain.Min;
            var scale = Vector4.Subtract(domain.Max, domain.Min);
            return new Vector4((_vtx & 0x1FFFFF) / 2097151f * scale.X + offset.X,
                ((_vtx >> 21) & 0x1FFFFF) / 2097151f * scale.Y + offset.Y,
                ((_vtx >> 42) & 0x3FFFFF) / 4194303f * scale.Z + offset.Z, 1f);
        }
    }

    public class BlenderMeshContainer
    {
        public string Name;

        public List<List<int>> Primitives;

        public List<Vector4> Vertices;

        public BlenderMeshContainer(string name)
        {
            Name = name;
            Vertices = new List<Vector4>();
            Primitives = new List<List<int>>();
        }

        public BlenderMeshContainer Offset(float offsetX, float offsetY, float offsetZ)
        {
            for (var i = 0; i < Vertices.Count; i++)
                Vertices[i] = new Vector4(
                    Vertices[i].X + offsetX,
                    Vertices[i].Y + offsetY,
                    Vertices[i].Z + offsetZ,
                    Vertices[i].W);

            return this;
        }
    }

    public static class Converter
    {
        public static List<BlenderMeshContainer> Convert(string path, bool offsetTeraMesh, float tileSize,
            Vector3 teraMeshOffset)
        {
            using var fs = File.OpenRead(path);

            var root = (hkRootLevelContainer) Util.ReadBotwHKX(fs, Path.GetExtension(path)).Last();

            if (root.m_namedVariants[0].m_className != "hkpRigidBody" || !offsetTeraMesh) return root.ToMesh();

            var baseName = Path.GetFileNameWithoutExtension(path);
            var xz = (from coord in baseName!.Split("-")
                select int.Parse(coord)).ToList();
            return (from meshContainer in root.ToMesh()
                    select meshContainer.Offset(
                        teraMeshOffset.X + tileSize * xz[0],
                        teraMeshOffset.Y,
                        teraMeshOffset.Z + tileSize * xz[1]))
                .ToList();
        }
    }
}