#!/bin/bash
for i in {131..145}
do
    RESOURCE_ID=$(cat resources.txt | head -n $i | tail -n 1 | xargs -i echo -n {})
    cd ../../
    ./hydrotest hydroshare PerformanceTestSuite.test_D_000001 --resource $RESOURCE_ID --grid selenium --browser chrome &
    cd scripts/hs_resource_creation
done
