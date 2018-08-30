#!/usr/bin/env bash

display_usage() {
    echo "*** CUAHSI HydroClient Performance Testing Execution ***"
    echo "usage: $0 [test] [users] [delay] [browser]  # execute HydroClient test number [test] and wait [delay] seconds"
    echo "                                            # between each of the [users] successive simulated users."
    echo "                                            # setup each of the users with a [browser] browser (all have OS Linux)"
}

# Display usage if != 4 argument provided
if [  $# -ne 4 ]
then
    display_usage
    exit 1
fi

cd ../..

for i in $(seq 1 1 $2)
do
    echo "Simulating user $i"
    ./hydrotest hydroclient "HydroclientTestSuite.test_A_$1" --grid localhost --browser "$4" &> "user-$i-results.txt" &
    sleep $3
done

sleep 120  # ensure tests have finished
DATETIME=$(date -I'minutes')
for i in $(seq 1 1 $2)
do
    cat "user-$i-results.txt" >> "scripts/hc_performance_testing/$1_$2_$3_$4_$DATETIME.txt"
done
rm -f ../user-*.txt

