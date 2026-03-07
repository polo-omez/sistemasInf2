#!/bin/bash

SCRIPT=$1
if [ -z "$SCRIPT" ]; then
    echo "Error: Use example: ./metrics.sh read_1000_entries.py"
    exit 1
fi

TIMES=()
echo "" 
echo "| Iteration | Time elapsed (seg) |"
echo "|:---------:|:------------------:|"

for i in {1..7}
do
    OUT=$(python3 "$SCRIPT")
    T=$(echo "$OUT" | grep -oP '\d+\.\d+')
    TIMES+=($T)
    echo "|     $i     |      $T      |"
done
echo "|___________|____________________|"

STATS=$(python3 -c "
import statistics as s
import sys
data = [float(x) for x in sys.argv[1:]]
print(f'{s.mean(data):.6f}|{s.stdev(data):.6f}')
" "${TIMES[@]}")

MEAN=$(echo $STATS | cut -d'|' -f1)
STDEV=$(echo $STATS | cut -d'|' -f2)

echo ""
echo "----------Stats resume:-----------"
echo "|   Mean    | Standard Deviation |"
echo "|:---------:|:------------------:|"
echo "| $MEAN  |      $STDEV      |"
echo "|___________|____________________|"
echo "" 
