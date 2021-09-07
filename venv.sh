#!/bin/bash

cd $(dirname $0)

[ ! -d "./venv/" ] &&
	echo "venv doesn't exist, creating..." &&
	python -m venv ./venv/ &&
	echo "venv created! sourcing..." &&
	source ./venv/bin/activate &&
	echo "installing deps..." &&
	python -m pip install -r ./requirements.txt &&
	echo "done! use 'source ./venv/bin/activate' to use! exiting..." &&
	exit 0

echo "venv already exists, use 'source ./venv/bin/activate' to use! exiting..." &&
	exit 0
