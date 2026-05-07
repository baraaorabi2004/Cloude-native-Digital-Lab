# 1. Base Image
FROM ubuntu:22.04

# Define environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    DISPLAY=:1 \
    VNC_PORT=5901 \
    NO_VNC_PORT=8080 \
    USER=cisco \
    HOME=/home/cisco

# 2. Install Core Dependencies & THE ENTIRE Qt5 ENVIRONMENT
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        xvfb x11vnc novnc websockify xfce4 xfce4-terminal wget curl ca-certificates sudo dbus-x11 x11-xserver-utils libssl-dev libnss3 libasound2 libpulse0 libxss1 libxcb-xinerama0 libxcb-randr0 libxcb-shape0 libxcb-xfixes0 libxkbcommon-x11-0 libgl1-mesa-glx libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxcb-util1 libxrender1 libfontconfig1 libdbus-1-3 libx11-xcb1 libglib2.0-0 python3 net-tools \
        libqt5gui5 libqt5network5 libqt5widgets5 libqt5sql5 libqt5xml5 libqt5core5a libqt5webenginewidgets5 libqt5webengine5 libqt5script5 libqt5scripttools5 libqt5multimedia5 libqt5texttospeech5 libqt5printsupport5 libqt5svg5 libqt5x11extras5 libqt5opengl5 libqt5quick5 libqt5qml5 libqt5websockets5 libqt5networkauth5 libcanberra-gtk-module libcanberra-gtk3-module libdouble-conversion3 libxcb-xinerama0 libxcb-xinput0 libxcb-xkb1 libxkbcommon0 libxkbcommon-x11-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 3. Install Cisco Packet Tracer
COPY PacketTracer.deb /tmp/PacketTracer.deb
RUN echo "packettracer packettracer/accept-eula boolean true" | debconf-set-selections && \
    (dpkg -i /tmp/PacketTracer.deb || apt-get install -fy) && \
    if [ ! -d "/opt/pt" ]; then dpkg-deb -x /tmp/PacketTracer.deb /; fi && \
    # Point to the official launch script, NOT the binary directly
    ln -sf /opt/pt/packettracer /usr/local/bin/packettracer && \
    ldconfig && \
    rm /tmp/PacketTracer.deb

# 4. Create User
RUN useradd -m -s /bin/bash -G sudo ${USER} && \
    echo "${USER}:cisco123" | chpasswd && \
    echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN ln -s /usr/share/novnc/vnc.html /usr/share/novnc/index.html
WORKDIR ${HOME}

# 5. Startup Script
COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

ENV PORT 8080
EXPOSE 8080
USER ${USER}
CMD ["/startup.sh"]