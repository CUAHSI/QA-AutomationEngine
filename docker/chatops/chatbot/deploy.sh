#!/usr/bin/env bash

NAME=$(echo "$2" | sed 's/\./-/g' | sed 's/ /-/g' | tr '[:upper:]' '[:lower:]')

WS_CLIENT_SECRET=$(echo $NAME | sha256sum | head -c32)
WS_ENCRYPTION_KEY=$(echo $NAME | sha256sum | head -c16)
DOMAIN=$NAME.$ROOT_DOMAIN

if [ "$1" == "workstation" ]
then
    gcloud auth activate-service-account --key-file /etc/webhooks/google.json
    cat /etc/webhooks/google.json | docker login -u _json_key --password-stdin https://us.gcr.io
    gcloud container clusters get-credentials $CLUSTER --zone $ZONE
    kubectl create namespace $NAME
    cp /etc/webhooks/google.json google.json
    kubectl create secret generic google-json --from-file=google.json --namespace $NAME > /proc/1/fd/1 2>&1
    rm google.json
    cd helm
    helm dep update
    helm upgrade $NAME-workstation . --install \
        --namespace $NAME \
        --set domain=$DOMAIN  \
        --set clientSecret=$WS_CLIENT_SECRET \
        --set encryptionKey=$WS_ENCRYPTION_KEY \
        --set docker.registry=$REPO \
        --set certbot.email=$EMAIL \
        --set passwd=$NAME \
        --set components.selenium.enabled=true \
        --set components.landing.enabled=true \
        --set landing.image=$LANDING_IMAGE \
        --set landing.targetPort=80 > /proc/1/fd/1 2>&1
    for i in {1..300}
    do
        IP=$(kubectl get services --namespace $NAME -o custom-columns=NAME:.status.loadBalancer.ingress[0].ip --no-headers | grep -e "[0-9].*[0-9]")
        if [ ! -z $IP ]; then
            gcloud dns --project=$PROJECT record-sets transaction start --zone=$DNS_ZONE > /proc/1/fd/1 2>&1
            gcloud dns --project=$PROJECT record-sets transaction add $IP --name=$DOMAIN. --ttl=300 --type=A --zone=$DNS_ZONE > /proc/1/fd/1 2>&1
            gcloud dns --project=$PROJECT record-sets transaction execute --zone=$DNS_ZONE > /proc/1/fd/1 2>&1
            curl -X POST $3 -d "
                {
                    \"text\": \"Your workstation will be ready in a minute or two (DNS subdomain A record propagation).  The username is workstation and password is $NAME.  Get started at https://$DOMAIN.\",
                    \"response_type\": \"in_channel\"
                }" > /proc/1/fd/1 2>&1
            exit 0
        else
            sleep 5
        fi
    done
    curl -X POST $3 -d "
    {
        \"text\": \"Workstation could not be created.\",
        \"response_type\": \"in_channel\"
    }" > /proc/1/fd/1 2>&1
fi