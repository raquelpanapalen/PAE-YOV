#!/bin/bash
# Script that does some preprocessing on the recorded database_size
# Author: aaaaluki

# Includes
. $(dirname "$0")/utils.sh

# Global variables
DATABASE_FOLDER=""
OUTPUT_FOLDER=""
OUTPUT_SAMPLE_RATE=22050

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
    meta_files=$(ls $DATABASE_FOLDER | grep -vE "\.wav$")

    # Copy the meta files (metadata, license, others...) to the created folder
    for mfile in $meta_files; do
        cp -r "${DATABASE_FOLDER}/${mfile}" "${OUTPUT_FOLDER}/${mfile}"
    done

    # So some processing on the database files
    i=0
    for file in $database_files
    do
        out_file="${OUTPUT_FOLDER}/$(basename $file)"

        # Resample file to 22050 Hz and mix all input channels
        sox $file -r $OUTPUT_SAMPLE_RATE $out_file remix -

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
