#!/bin/bash
for i in {0..0}
do
    for j in {131..150}
    do
        k=$((i * 12 + j))
        RESOURCE_ID=$(cat resources.txt | head -n "$k" | tail -n 1 | xargs -i echo -n {})
        cd ../../
        ./hydrotest hydroshare PerformanceTestSuite.test_D_000001 --resource $RESOURCE_ID --grid selenium --browser chrome &
        cd scripts/hs_resource_creation
    done
done
