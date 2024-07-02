#!/bin/bash
set -e

# t1="2024-07-01T00:00:00"
# t2="2024-07-01T12:00:00"

t1="2024-07-01T12:00:00"
t2="2024-07-01T23:59:00"

# t1="2024-07-02T00:00:00"
# t2="2024-07-02T12:00:00"

echo "Filtering logs between $t1 and $t2 ..."

# iterate recursively over all .log files
# for file in $(find logs/ -name "*.log"); do
for file in $(find logs/ -name "ovh-rbuilder-04.log"); do
    echo $file

    # create temp file
    temp_file=$(mktemp)
    echo "Filtering relevant entries into $temp_file ..."
    grep finalize_time_ms $file | sed 's/.*: //' | grep "^{" >> $temp_file

    temp_file2=$(mktemp)
    echo "Filtering date range into $temp_file2 ..."
    jq -c --arg t1 "$t1" --arg t2 "$t2" 'select ((.timestamp >= $t1) and (.timestamp < $t2))' $temp_file > $temp_file2


    echo "Extracting data into output.csv ..."
    rm -f output.csv
    python3 logs_scripts/extract_data_csv.py $temp_file2

    echo -e "Lines of input: \t $( wc -l < $temp_file2 )"
    echo -e "Lines of output.csv: \t $( wc -l < output.csv )"
    # wc -l output.csv

    echo "Generating stats ..."
    python3 logs_scripts/gen_stats.py output.csv

    echo ""
    echo ""

    # remove temp files
    rm $temp_file
    rm $temp_file2
done
