FROM selenium/node-chrome

USER root
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -qqy \
    && apt-get install -qqy supervisor \
        openssh-server \
        xfce4 xfce4-goodies \
        x11vnc \
        speedtest-cli \
        emacs \
    && apt-get autoclean -qqy \
	  && apt-get autoremove -qqy \
	  && rm -rf /var/lib/apt/lists/*

# Prepare VNC
RUN mkdir -p ~/.vnc \
  && x11vnc -storepasswd 'cuahsi@secret' ~/.vnc/passwd

# Prepare ssh server
RUN mkdir -p /var/run/sshd

ADD node-debug-common/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD node-debug-common/startup.sh /opt/bin/startup.sh

EXPOSE 22
EXPOSE 5900
