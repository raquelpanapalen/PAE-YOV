#!/bin/bash
# Script that does some preprocessing on the recorded database_size
# Author: aaaaluki

# Includes
. $(dirname "$0")/utils.sh

# Global variables
ADD_POINTS_SCRIPT="$(dirname $0)/add_points.py"
DATABASE_FOLDER=""
OUTPUT_FOLDER=""
OUTPUT_SAMPLE_RATE=16000

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

        if [[ "$mfile" =~ \.txt$ ]]; then
            out_mfile="$(basename $mfile .txt)_norm.txt"
            _info_msg "Adding points to \"${DATABASE_FOLDER}/${mfile}\" into \"${OUTPUT_FOLDER}/${out_mfile}\""
            $ADD_POINTS_SCRIPT "${DATABASE_FOLDER}/${mfile}" "${OUTPUT_FOLDER}/${out_mfile}" > /dev/null
        fi
    done

    # So some processing on the database files
    db_time_before=$(soxi -D $DATABASE_FOLDER/*.wav | awk '{s+=$1} END {printf("time[hh:mm:ss] -> %02d:%02d:%02.2f\n", s/3600, s%3600 / 60, s%60)}')
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
    db_time_after=$(soxi -D $OUTPUT_FOLDER/*.wav | awk '{s+=$1} END {printf("time[hh:mm:ss] -> %02d:%02d:%02.2f\n", s/3600, s%3600 / 60, s%60)}')
    _info_msg "Procesing finished!"
    _info_msg "Time before processing: ${db_time_before}"
    _info_msg "Time after processing: ${db_time_after}"
}

# Hide cursor while running script
trap _cleanup EXIT
tput civis

main $@

