#!/bin/bash

sudo apt-get update
sudo apt-get -y install unzip
cd /
cd opt
mkdir terraform && cd $_
curl -o terraform.zip https://releases.hashicorp.com/terraform/0.11.1/terraform_0.11.1_linux_amd64.zip
unzip terraform.zip
sudo touch /etc/profile.d/envvar.sh
echo export PATH=/opt/terraform/:$PATH | sudo tee /etc/profile.d/envvar.sh
sudo rm terraform.zip
