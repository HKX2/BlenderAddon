#!/bin/bash

cd $(dirname $0)

rm -rf ./build/
mkdir ./build/

cp -r ./blenderaddon_hkx2/ ./build/

dotnet build ./lib/BlenderAddon/BlenderAddon.sln

mkdir ./build/blenderaddon_hkx2/lib/
cat >./build/blenderaddon_hkx2/lib/net5.0.runtimeconfig.json <<-EOF
	{
	  "runtimeOptions": {
	    "tfm": "net5.0",
	    "framework": {
	      "name": "Microsoft.NETCore.App",
	      "version": "5.0.2"
	    }
	  }
	}
EOF
cp ./lib/BlenderAddon/BlenderAddon/bin/Debug/net5.0/*.{so,dll} ./build/blenderaddon_hkx2/lib/

if [[ $1 == "test" ]]; then
	rm -rf ~/.config/blender/2.93/scripts/addons/blenderaddon_hkx2
	cp -r ./build/blenderaddon_hkx2 ~/.config/blender/2.93/scripts/addons/
	rm -rf ./build/
fi

if [[ $1 == "publish" ]]; then
	pushd ./build/
	zip -r ../blenderaddon_hkx2.zip ./blenderaddon_hkx2
	popd
	rm -rf ./build/
fi
