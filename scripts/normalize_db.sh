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
    echo "Usage: $0 <database_folder> <output_database>"
    exit 1
}

function _setup() {
    [[ $# -lt 2 ]] && _error_msg "Give a database folder" && _usage

    DATABASE_FOLDER="$(dirname $1)/$(basename $1)"
    OUTPUT_FOLDER="$(dirname $2)/$(basename $2)"

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

        # Resample file to "OUTPUT_SAMPLE_RATE Hz" and mix all input channels,
        # then remove beginning and trailing silences
        # For the silence part of this command I used the following guide:
        # https://digitalcardboard.com/blog/2009/08/25/the-sox-of-silence/
        # Description of each step:
        # - Resample
        # - Join all channels into one
        # - Normalize to -3 dB (max value is at -3dB)
        # - Trim beginning silences
        # - Reverse audio
        # - Trim ending silences
        # - Reverse audio
        sox $file -r $OUTPUT_SAMPLE_RATE $out_file \
            remix - \
            gain -n -3 \
            vad \
            reverse \
            vad \
            reverse

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

