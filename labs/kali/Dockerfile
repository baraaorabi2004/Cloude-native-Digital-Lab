# 1. Use a minimal base image to save resources (Sustainability)
FROM kalilinux/kali-rolling:latest

# Define environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    VNC_PORT=6901 \
    USER=kali \
    HOME=/home/kali \
    KASM_VNC_VERSION=1.3.2

# 2 & 3. Install KasmVNC for web-based GUI access and pre-install Nmap/Metasploit
RUN apt-get update && \
    apt-get upgrade -y && \
    # Install core tools, XFCE desktop environment, and security tools
    apt-get install -y --no-install-recommends \
        nmap \
        metasploit-framework \
        xfce4 \
        xfce4-terminal \
        wget \
        curl \
        ca-certificates \
        sudo \
        ssl-cert \
        libgetopt-long-descriptive-perl \
        libdata-dump-perl \
        libssl-dev \
        libnss3 \
        dbus-x11 \
        x11-xserver-utils && \
    # Download and install KasmVNC
    wget https://github.com/kasmtech/KasmVNC/releases/download/v${KASM_VNC_VERSION}/kasmvncserver_kali-rolling_${KASM_VNC_VERSION}_amd64.deb -O /tmp/kasmvnc.deb && \
    apt-get install -y /tmp/kasmvnc.deb && \
    # Clean up to keep the image minimal and optimized
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create a non-root user (Standard practice for Cloud Run/GKE security)
RUN useradd -m -s /bin/bash -G sudo ${USER} && \
    echo "${USER}:${USER}" | chpasswd && \
    echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Setup environment for the user
USER ${USER}
WORKDIR ${HOME}

# Configure KasmVNC for the user
RUN mkdir -p ${HOME}/.vnc && \
    # Setup VNC password
    echo "kali" | vncpasswd -f > ${HOME}/.vnc/passwd && \
    chmod 600 ${HOME}/.vnc/passwd && \
    # Create an XFCE startup script
    printf "#!/bin/bash\nexport DISPLAY=:1\nstartxfce4 &\n" > ${HOME}/.vnc/xstartup && \
    chmod +x ${HOME}/.vnc/xstartup

# 4. Ensure the container is optimized for Google Cloud Run or GKE deployment
# Expose the requested port for web-based GUI access
EXPOSE 6901

# Start KasmVNC and tail the log so the container remains running for Cloud Run
CMD vncserver :1 -depth 24 -geometry 1280x720 -websocketPort ${VNC_PORT} && tail -f ${HOME}/.vnc/*.log