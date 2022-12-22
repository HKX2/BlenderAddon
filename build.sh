#!/bin/bash

[[ -z "$1" ]] && echo "no argument provided!" && exit 255

cd "$(dirname "$0")"

rm -rf ./build/
mkdir ./build/

cp -r ./blenderaddon_hkx2/ ./build/

dotnet build ./lib/BlenderAddon/BlenderAddon.sln

mkdir ./build/blenderaddon_hkx2/lib/
cp ./lib/BlenderAddon/BlenderAddon/bin/Debug/net5.0/*.{so,dll} ./build/blenderaddon_hkx2/lib/

if [[ "$1" == "test" ]]; then
  for VERSION in "$HOME"/.config/blender/*; do
    ADDONS_DIR="$VERSION/scripts/addons"
    mkdir -p "$ADDONS_DIR"
    rm -rf "$ADDONS_DIR"/blenderaddon_hkx2
    cp -r {./build,"$VERSION"/scripts/addons}/blenderaddon_hkx2
  done
  rm -rf ./build/
fi

if [[ "$1" == "publish" ]]; then
  pushd ./build/
  7z a ../blenderaddon_hkx2.zip ./blenderaddon_hkx2
  popd
  rm -rf ./build/
fi
