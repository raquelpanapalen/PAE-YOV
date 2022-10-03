# Some useful functions for bash scripting (logging, displaying progress ...)
# Author: aaaaluki

CC_RED=$(echo -e "\033[0;31m")
CC_GREEN=$(echo -e "\033[0;32m")
CC_YELLOW=$(echo -e "\033[0;33m")
CC_END=$(echo -e "\033[0m")

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

