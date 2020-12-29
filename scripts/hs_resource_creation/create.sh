#!/bin/bash
wget https://hydroshare.org/resource/f87be11d9ff54a0489d8f1b12588b453/data/contents/Jupyter-notebooks-and-workflows-on-Hydroshare.pdf
wget https://hydroshare.org/resource/f87be11d9ff54a0489d8f1b12588b453/data/contents/Waterhackweek_-_January_24_2019_-_Tony_Castronova_CUAHSI.mp4
wget https://hydroshare.org/resource/f87be11d9ff54a0489d8f1b12588b453/data/contents/taudem.ipynb
for i in {1..15}
do
    for j in {9..20}
    do
        cp resource.json resource-$i-$j.json
        sed -i "s/XXXX/A-$i-$j/g" resource-$i-$j.json
        RESOURCE_ID=$(curl -u "$HS_USERNAME:$HS_PASSWORD" -H 'Accept: application/json' -H 'Content-Type: application/json' -X POST --data-binary @resource-$i-$j.json https://beta.hydroshare.org/hsapi/resource/ | jq .resource_id | sed 's/"//g')
        echo $RESOURCE_ID >> resources.txt
        sleep 1
        for k in $( eval echo {0..$j} )
        do
            cp Jupyter-notebooks-and-workflows-on-Hydroshare.pdf Jupyter-notebooks-and-workflows-on-Hydroshare-$k.pdf
            curl -u "$HS_USERNAME:$HS_PASSWORD" -X POST -H "Content-Type: multipart/form-data" -F "file=@Jupyter-notebooks-and-workflows-on-Hydroshare-$k.pdf" https://beta.hydroshare.org/hsapi/resource/$RESOURCE_ID/files/
            rm Jupyter-notebooks-and-workflows-on-Hydroshare-$k.pdf
            sleep 0.5
            cp Waterhackweek_-_January_24_2019_-_Tony_Castronova_CUAHSI.mp4 Waterhackweek_-_January_24_2019_-_Tony_Castronova_CUAHSI-$k.mp4
            curl -u "$HS_USERNAME:$HS_PASSWORD" -X POST -H "Content-Type: multipart/form-data" -F "file=@Waterhackweek_-_January_24_2019_-_Tony_Castronova_CUAHSI-$k.mp4" https://beta.hydroshare.org/hsapi/resource/$RESOURCE_ID/files/
            rm Waterhackweek_-_January_24_2019_-_Tony_Castronova_CUAHSI-$k.mp4
            sleep 0.5
            cp taudem.ipynb taudem-$k.ipynb
            curl -u "$HS_USERNAME:$HS_PASSWORD" -X POST -H "Content-Type: multipart/form-data" -F "file=@taudem-$k.ipynb" https://beta.hydroshare.org/hsapi/resource/$RESOURCE_ID/files/
            rm taudem-$k.ipynb
            sleep 0.5
        done
    done
done