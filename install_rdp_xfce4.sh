#!/bin/bash

# Update package lists
sudo apt update

# Install xrdp
sudo apt install -y xrdp

# Start xrdp service
sudo systemctl enable --now xrdp

# Install xfce desktop environment (you can choose a different desktop environment if you prefer)
sudo apt install -y xfce4

# Configure xrdp to use xfce
echo xfce4-session > ~/.xsession

# Restart xrdp service
sudo systemctl restart xrdp

echo "RDP server installation complete. You can now connect to this machine using an RDP client."
