#!/usr/bin/env bash

# Start VNC server & XFCE desktop environment in all service containers
docker ps -q --filter name=chrome | while read id; do docker exec $id /opt/bin/startup.sh; done
docker ps -q --filter name=firefox | while read id; do docker exec $id /opt/bin/startup.sh; done
