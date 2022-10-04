#!/bin/bash
# Script that does some preprocessing on the recorded database_size
# Author: aaaaluki

# Includes
. $(dirname "$0")/utils.sh

# Global variables
DATABASE_FOLDER=""
OUTPUT_FOLDER=""

function _usage() {
    echo "Usage: $0 <database_folder>"
    exit 1
}

function _setup() {
    [[ $# -lt 1 ]] && _error_msg "Give a database folder" && _usage

    DATABASE_FOLDER="$(dirname $1)/$(basename $1)"
    OUTPUT_FOLDER="${DATABASE_FOLDER}_normalized"

    if [ -d $OUTPUT_FOLDER ]; then
        _warn_msg "Directory ${OUTPUT_FOLDER} exists, overwriting!"
    else
        mkdir $OUTPUT_FOLDER
    fi
}

function _cleanup() {
    tput cnorm
}

function main() {
    _setup $@

    _info_msg "Procesing WAVs from \"${DATABASE_FOLDER}\" into \"${OUTPUT_FOLDER}\""
    database_files=$(ls $DATABASE_FOLDER/*.wav)
    database_size=$(ls $DATABASE_FOLDER/*.wav | wc -l)

    i=0
    for file in $database_files
    do
        # So some processing on the input file
        out_file="${OUTPUT_FOLDER}/$(basename $file)"

        # Duplicate left channel to L and R
        sox $file $out_file remix 1 1

        _progress $i $database_size
        i=$(( i+=1 ))
    done
    _progress $i $database_size && echo
    _info_msg "Procesing finished!"
}

# Hide cursor while running script
trap _cleanup EXIT
tput civis

main $@
