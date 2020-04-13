# Developer Workstation Hub

1. Change the payload token value in [chatops/chatbot/hooks.json](chatops/chatbot/hooks.json) - use the value from a new Slack webhook integration
1. Configure docker to use the organizational Google Cloud Container Registry
1. Configure kubectl to use the organizational Google Kubernetes Engine cluster
1. Get a google.json keyfile for a Google Cloud Platform service account, with Google Cloud DNS and Google Kubernetes Engine permissions
1. Create a kubernetes secret --from-file, call it google-json and use the file google.json
    1. `kubectl create secret generic google-json --from-file google.json`
    1. Delete the google.json after the secret is created
1. From [docker/chatops/chatbot](docker/chatops/chatbot), build and push the docker image
1. From [docker/chatops/getting-started](docker/chatops/getting-started), build and push the docker image
1. Build and push docker images from https://github.com/ndebuhr/cloud-native-workstation#build
1. From [docker/chatops/helm](docker/chatops/helm)
    ```
    helm upgrade chatbot . --install \
        --set project=YOURGCPPROJECT \
        --set cluster=YOURCLUSTER \
        --set zone=YOURCLUSTERZONE \
        --set image=us.gcr.io/YOURREPO/CHATBOTIMAGENAME:YOURTAG \
        --set repo=us.gcr.io/YOURREPO \
        --set landingImage=us.gcr.io/YOURREPO/LANDINGPAGEIMAGENAME:YOURTAG \
        --set rootDomain=YOURDOMAIN.com \
        --set dnsZone=YOURDNSZONE \
        --set email=YOUREMAIL@YOURDOMAIN.com
    ```
1. Set the resulting LoadBalancer IP from the helm install as a Slack endpoint

