#!/bin/bash

# Ensure Clean State
rm -rf /tmp/.X1-lock /tmp/.X11-unix/X1

# Essential: Set Library Path for Packet Tracer
export LD_LIBRARY_PATH=/opt/pt/lib:/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH

# 1. Start Xvfb
Xvfb :1 -screen 0 1280x800x24 &
sleep 2

# 2. Start XFCE
export DISPLAY=:1
startxfce4 &
sleep 3

# 3. Start x11vnc
x11vnc -display :1 -nopw -forever -shared -bg -rfbport 5901 -listen localhost &
sleep 2

# 4. Start noVNC Bridge
echo "Starting noVNC Bridge on Port ${PORT}..."
/usr/share/novnc/utils/launch.sh --vnc localhost:5901 --listen ${PORT}