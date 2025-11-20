#!/bin/bash


docker build . -t microk8s-1:32000/ai-toolbox:latest

# microk8s ctr image pull microk8s-1:32000/ai-toolbox:latest
# microk8s kubectl create deployment nginx --image=10.141.241.175:32000/mynginx:registry

microk8s kubectl apply -f microk8s_deployment.yaml