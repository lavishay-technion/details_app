#!/usr/bin/env bash
################################################
# Created by Alex M. Schapelle AKA silent-mobius
# Purpose: buils script for making this project work
# Version: 0.0.1
# Date: 14.06.2024
#################################################
APP_VERSION=${1:'0.0.1'}
docker build . -t details_app


# kubeadm token create --print-join-command
# kubeadm join 192.168.64.7:6443 --token d6pmk7.2jyxgmf97juceo08 --discovery-token-ca-cert-hash sha256:43a9eda442dd94bfe2fc0875846514c588599dbd40c98c6c8a713ef1fac1e4c4