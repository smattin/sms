#!/bin/env -S bash
#
# set -x

# repeatedly output last line of $SUMMARY_FILE until find "sent $MESSAGES"
MESSAGES="${MESSAGES:-100}"
SUMMARY_FILE="${SUMMARY_FILE:-summary.txt}"
UPDATE_RATE="${UPDATE_RATE:-10}"
CMD="tail -1 $SUMMARY_FILE"

# summary file exists and is readable
while test -f "$SUMMARY_FILE" -a -r "$SUMMARY_FILE"; do
        SUMMARY=`$CMD`
        echo "$SUMMARY"
        # check if summary says all messages sent
        # SAM ??? is test really more portable than [[ ?
        if [[ "$SUMMARY" == "sent ${MESSAGES}"* ]]
        then
                break 2
        fi
        sleep $UPDATE_RATE
done
