#!/bin/bash
wget https://hydroshare.org/resource/f87be11d9ff54a0489d8f1b12588b453/data/contents/Jupyter-notebooks-and-workflows-on-Hydroshare.pdf
wget https://hydroshare.org/resource/f87be11d9ff54a0489d8f1b12588b453/data/contents/Waterhackweek_-_January_24_2019_-_Tony_Castronova_CUAHSI.mp4
wget https://hydroshare.org/resource/f87be11d9ff54a0489d8f1b12588b453/data/contents/taudem.ipynb
for i in {0..150}
do
    cp resource.json resource-$i.json
    sed -i "s/XXXX/$i/g" resource-$i.json
    RESOURCE_ID=$(curl -u "$HS_USERNAME:$HS_PASSWORD" -H 'Accept: application/json' -H 'Content-Type: application/json' -X POST --data-binary @resource-$i.json https://cuahsi-dev-1.hydroshare.org/hsapi/resource/ | jq .resource_id | sed 's/"//g')
    echo $RESOURCE_ID >> resources.txt
    sleep 1
    curl -u "$HS_USERNAME:$HS_PASSWORD" -X POST -H "Content-Type: multipart/form-data" -F "file=@Jupyter-notebooks-and-workflows-on-Hydroshare.pdf" https://cuahsi-dev-1.hydroshare.org/hsapi/resource/$RESOURCE_ID/files/
    sleep 0.5
    curl -u "$HS_USERNAME:$HS_PASSWORD" -X POST -H "Content-Type: multipart/form-data" -F "file=@Waterhackweek_-_January_24_2019_-_Tony_Castronova_CUAHSI.mp4" https://cuahsi-dev-1.hydroshare.org/hsapi/resource/$RESOURCE_ID/files/
    sleep 0.5
    curl -u "$HS_USERNAME:$HS_PASSWORD" -X POST -H "Content-Type: multipart/form-data" -F "file=@taudem.ipynb" https://cuahsi-dev-1.hydroshare.org/hsapi/resource/$RESOURCE_ID/files/
    sleep 0.5
done
