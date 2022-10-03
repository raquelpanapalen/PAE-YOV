#!/bin/bash

CC_RED=$(echo -e "\033[0;31m")
CC_GREEN=$(echo -e "\033[0;32m")
CC_YELLOW=$(echo -e "\033[0;33m")
CC_END=$(echo -e "\033[0m")

DATABASE_FOLDER=""
OUTPUT_FOLDER=""

function _usage() {
    echo "Usage: $0 <database_folder>"
    exit 1
}

function _info_msg() {
    echo "${CC_GREEN}[I]${CC_END} ${1}"
}

function _warn_msg() {
    echo "${CC_YELLOW}[W]${CC_END} ${1}"
}

function _error_msg() {
    echo "${CC_RED}[E]${CC_END} ${1}"
}

function _progress() {
    # $1: iteration number
    # $2: total iterations
    # $N: width of the progress bar
    local N=40
    local completed=$(( ($N*$1)/$2 ))
    local i=0

    echo -n "${CC_YELLOW}[${CC_GREEN}"
    for ((i = 0 ; i < $completed ; i+=1)); do
        echo -n "#"
    done

    echo -n "${CC_RED}"
    for ((i = $completed ; i < $N ; i+=1)); do
        echo -n "."
    done
    echo -n "${CC_YELLOW}]${CC_END} (${1}/${2})"
    printf "\r"
}

function _setup() {
    [[ $# -lt 1 ]] && _error_msg "Give a database folder" && _usage

    DATABASE_FOLDER=$1
    OUTPUT_FOLDER="${DATABASE_FOLDER}_normalized"

    if [ -d $OUTPUT_FOLDER ]; then
        _warn_msg "Directory ${OUTPUT_FOLDER} exists, overwriting!"
    else
        mkdir $OUTPUT_FOLDER
    fi
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

main $@
