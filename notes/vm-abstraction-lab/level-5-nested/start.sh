#!/bin/bash
# Check KVM support
if [ -e /dev/kvm ]; then
    echo "KVM acceleration available"
else
    echo "KVM not available, using TCG acceleration"
fi

# Start libvirtd if available
if command -v libvirtd &> /dev/null; then
    libvirtd -d
fi

# Start VM manager API
python3 /app/vm_manager.py
