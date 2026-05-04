#!/bin/bash

case "$1" in
  start)
    echo "Starting VMs..."
    vagrant up
    echo "VMs started. Access web at http://localhost:3004"
    ;;
  stop)
    echo "Stopping VMs..."
    vagrant halt
    ;;
  destroy)
    echo "Destroying VMs..."
    vagrant destroy -f
    ;;
  ssh)
    vagrant ssh $2
    ;;
  status)
    vagrant status
    ;;
  *)
    echo "Usage: $0 {start|stop|destroy|ssh|status}"
    exit 1
    ;;
esac
