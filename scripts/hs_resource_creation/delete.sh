#!/bin/bash
for i in {1..190}
do
    RESOURCE_ID=$(cat resources.txt | head -n $i | tail -n 1 | xargs -i echo -n {})
    # Get a CSRF Token from Swagger API Delete Call
    curl -u "$HS_USERNAME:$HS_PASSWORD" -H "X-CSRFToken: $HS_CSRF_TOKEN" -X DELETE https://beta.hydroshare.org/hsapi/resource/$RESOURCE_ID/
    sleep 1
done
