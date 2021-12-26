#!/bin/bash

cd $(dirname $0)

rm -rf ./build/
mkdir ./build/

cp -r ./blenderaddon_hkx2/ ./build/

dotnet build ./lib/BlenderAddon/BlenderAddon.sln

mkdir ./build/blenderaddon_hkx2/lib/
cat >./build/blenderaddon_hkx2/lib/net6.0.runtimeconfig.json <<-EOF
	{
	  "runtimeOptions": {
	    "tfm": "net6.0",
	    "framework": {
	      "name": "Microsoft.NETCore.App",
	      "version": "6.0.0"
	    }
	  }
	}
EOF
cp ./lib/BlenderAddon/BlenderAddon/bin/Debug/net5.0/*.{so,dll} ./build/blenderaddon_hkx2/lib/

if [[ $1 == "test" ]]; then
  for version in ~/.config/blender/*; do
    rm -rf $version/scripts/addons/blenderaddon_hkx2/
    cp -r ./build/blenderaddon_hkx2/ $version/scripts/addons/
  done
  rm -rf ./build/
fi

if [[ $1 == "publish" ]]; then
  pushd ./build/
  zip -r ../blenderaddon_hkx2.zip ./blenderaddon_hkx2
  popd
  rm -rf ./build/
fi
