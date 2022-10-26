#!/bin/bash
# Rename filenames on a database padding the numbers

function _usage() {
    echo "Usage: $0 <database_folder> <file_prefix>"
    echo ""
    echo "Example:"
    echo -e "\t$0 databases/helena_cat helena_cat_"

    exit 1
}

[[ $# -lt 2 ]] && _usage

DB_FOLDER="$(dirname $1)/$(basename $1)"
FILE_PATTERN=$2
EXTENSION=".wav"
PADD_LENGTH=5

for f in $DB_FOLDER/$FILE_PATTERN[0-9]*$EXTENSION; do
    number=${f#$DB_FOLDER/$FILE_PATTERN}
    number=${number%$EXTENSION}
    out_file=$(printf "${DB_FOLDER}/${FILE_PATTERN}%0${PADD_LENGTH}d${EXTENSION}" $number)
    mv $f $out_file
done

