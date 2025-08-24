FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    qemu-system-x86 \
    qemu-utils \
    cloud-image-utils \
    bridge-utils \
    cpu-checker \
    libvirt-daemon-system \
    libvirt-clients \
    virtinst \
    curl \
    wget \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Flask for API
RUN pip3 install flask

# Create VM management API
COPY vm_manager.py /app/vm_manager.py
COPY start.sh /app/start.sh

WORKDIR /app

# Download a minimal Linux image
RUN wget -q http://download.cirros-cloud.net/0.6.2/cirros-0.6.2-x86_64-disk.img -O /app/vm-disk.img

EXPOSE 5000 5900

CMD ["/app/start.sh"]
