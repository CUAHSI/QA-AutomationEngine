#!/usr/bin/env bash

# start up supervisord, all daemons should launched by supervisord:
# 1. ssh server
# 2. XFCE desktop environment
# 3. VNC server
sudo /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
