#!/usr/bin/env bash

display_usage() {
    echo "*** CUAHSI HydroClient Performance Testing Execution ***"
    echo "usage: $0 [test] [users]  # execute HydroClient test number [test] using [users] simulated users"
}

# Display usage if != 2 argument provided
if [  $# -ne 2 ]
then
    display_usage
    exit 1
fi

cd ..

for i in $(seq 1 1 $2)
do
    echo "Simulating user $i"
    ./hydrotest hydroclient "HydroclientTestSuite.test_A_$1" --grid localhost &> "user-$i-results.txt" &
done
