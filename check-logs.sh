#!/bin/bash
#
# This script filters and analyzes logs from rbuilder, in particular to compare performance metrics.
#
# Output is saved in "./logs-analysis/".
#
# It looks for "Submitting bid" entries between a given date range:
#
#   {
#       "timestamp": "2024-06-30T15:31:42.352160Z",
#       "level": "DEBUG",
#       "fields": {
#           "message": "Submitting bid"
#       },
#       "target": "rbuilder::live_builder::building::relay_submit",
#       "span": {
#           "best_bid_value": "0.000074904023040978",
#           "bid_value": "0.020524330182794996",
#           "block": 20205414,
#           "buidler_name": "mp-ordering-cb",
#           "bundles": 85,
#           "fill_time_ms": "49",
#           "finalize_time_ms": "51",
#           "gas": 10741030,
#           "hash": "0xa773275f229ce224e6b1a9fda9eeea852bb58d2ec4db01ed6baa5eaaec3df558",
#           "true_bid_value": "0.020524330182794996",
#           "txs": 144,
#           "name": "bid"
#       },
#       "spans": []
#   }
#
set -e

t1="2024-07-02T00:00:00"
t2="2024-07-02T12:00:00"

echo "Filtering logs between $t1 and $t2 ..."

out_dir="logs-analysis"
rm -rf $out_dir
mkdir -p $out_dir

# iterate recursively over all .log files
for file in $(find logs/ -name "*.log"); do
    echo ""
    echo ""
    echo $file
    fn_base=$(basename $file .log)

    # 1. Filter relevant entries
    fn_filtered_logs="$out_dir/${fn_base}_filtered-logs.log"
    echo "Sanitizing logs and filtering relevant entries into $fn_filtered_logs ..."
    grep finalize_time_ms $file | sed 's/.*: //' | grep "^{" >> $fn_filtered_logs

    # 2. Filter date range
    fn_filtered_daterange="$out_dir/${fn_base}_filtered-logs-daterange.log"
    echo "Filtering date range into $fn_filtered_daterange ..."
    jq -c --arg t1 "$t1" --arg t2 "$t2" 'select (.fields.message == "Submitting bid" and (.timestamp >= $t1) and (.timestamp < $t2))' $fn_filtered_logs > $fn_filtered_daterange

    entries=$( wc -l < $fn_filtered_daterange )
    echo -e "Entries: \t $entries"
    if [ $entries -eq 0 ]; then
        echo "No entries to process, skipping to next file ..."
        continue
    fi

    # 3. Convert to TSV
    fn_tsv="$out_dir/${fn_base}.tsv"
    echo "Converting data to TSV into $fn_tsv ..."
    tsv_head="block\ttxs\tbundles\tgas\tfinalize_time_ms\tfill_time_ms\ttotal_time_ms"
    echo -e $tsv_head > $fn_tsv
    jq -r '[.span| (.block),(.txs),(.bundles),(.gas),(.finalize_time_ms|tonumber),(.fill_time_ms|tonumber),(.finalize_time_ms|tonumber)+(.fill_time_ms|tonumber)] | @tsv' $fn_filtered_daterange >> $fn_tsv

    # 4. Analyze data and get key stats
    fn_stats="$out_dir/${fn_base}_stats.txt"
    datamash -H --round=1 count 1 \
        mean 2 median 2 perc:90 2 perc:99 2 \
        mean 3 median 3 perc:90 3 perc:99 3 \
        mean 4 median 4 perc:90 4 perc:99 4 \
        mean 7 median 7 perc:90 7 perc:99 7 \
        < $fn_tsv > $fn_stats

    cat $fn_stats

    # 5. Plot data (toy)
    if command -v gnuplot &> /dev/null
    then
        fn_plot="$out_dir/${fn_base}_plot.png"
        echo "Plotting data into $fn_plot ..."
        gnuplot -e "set terminal png size 1024,768; set output '$fn_plot'; set datafile separator '\t'; set title '$fn_tsv'; plot '$fn_tsv' using (\$0):2 with lines title 'txs', '$fn_tsv' using (\$0):3 with lines title 'bundles'"
    fi
    # exit 0
done

# At the end, print all stats as one TSV block
FIRST=0
for file in $(find $out_dir -name "*_stats.txt"); do
    fn_base=$(basename $file _stats.txt)
    if [ $FIRST -eq 0 ]; then
        FIRST=1
        echo -e -n "file\t"
        sed -n '1p' $file
    fi
    echo -e -n "$fn_base\t"
    sed -n '2p' $file
done