#!/bin/bash


# For OSX development
if [[ `uname` == "Darwin" ]]; then
    script_directory=$(dirname "$0")
fi

# For Linux production deployment
if [[ `uname` == "Linux" ]]; then
    script_directory=$(dirname $(readlink -f $BASH_SOURCE))
fi

if [ -e $script_directory/lalookup.rc ]
then
	source $script_directory/lalookup.rc
else
	echo "WARN: $script_directory/lalookup.rc does not exist."
fi

exec $script_directory/env/bin/celery  -A LALookup beat -l DEBUG