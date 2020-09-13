#!/bin/bash
for i in {0..99}
do
    cp resource.json resource-$i.json
    sed -i "s/XXXX/$i/g" resource-$i.json
    RESOURCE_ID=$(curl -u "$HS_USERNAME:$HS_PASSWORD" -H 'Accept: application/json' -H 'Content-Type: application/json' -X POST --data-binary @resource-$i.json https://beta.hydroshare.org/hsapi/resource/ | jq .resource_id | sed 's/"//g')
    echo $RESOURCE_ID >> resources.txt
    sleep 1
    curl -u "$HS_USERNAME:$HS_PASSWORD" -X POST -H "Content-Type: multipart/form-data" -F "file=@files.zip" https://beta.hydroshare.org/hsapi/resource/$RESOURCE_ID/files/ > stdout.log 2> stderr.log
    sleep 1
done

