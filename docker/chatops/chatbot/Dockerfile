FROM ubuntu:18.04

USER root
ENV DEBIAN_FRONTEND noninteractive

# Install core utilities and dev tools
RUN apt-get update -qqy && \
  apt-get install -qqy apt-transport-https ca-certificates software-properties-common && \
  apt-get install -qqy git curl wget sudo && \
  apt-get install -qqy webhook

# Install gcloud cli
RUN export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
  echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" \
  | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
  apt-get update -y && apt-get install google-cloud-sdk -y

# Install kubectl, kubeadm, and kubelet
RUN RELEASE="$(curl -sSL https://dl.k8s.io/release/stable.txt)" && \
    curl -L --remote-name-all https://storage.googleapis.com/kubernetes-release/release/${RELEASE}/bin/linux/amd64/{kubeadm,kubelet,kubectl} && \
    install kubeadm /usr/local/bin/ && \
    install kubelet /usr/local/bin/ && \
    install kubectl /usr/local/bin/

# Install helm
RUN wget https://get.helm.sh/helm-v3.1.2-linux-amd64.tar.gz && \
    tar xfvz helm-v3.1.2-linux-amd64.tar.gz linux-amd64/helm && \
    install linux-amd64/helm /usr/local/bin/

RUN mkdir /etc/webhooks
RUN git clone https://github.com/ndebuhr/cloud-native-workstation /var/webhooks
ADD ./hooks.json /etc/webhooks/hooks.json
ADD ./deploy.sh /etc/webhooks/deploy.sh
RUN chmod +x /etc/webhooks/deploy.sh

EXPOSE 9000

ENTRYPOINT webhook -hooks /etc/webhooks/hooks.json -verbose