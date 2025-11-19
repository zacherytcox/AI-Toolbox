#!/bin/bash


docker build . -t microk8s-1:32000/ai-toolbox:latest

microk8s ctr image pull microk8s-1:32000/ai-toolbox:latest

microk8s kubectl apply -f microk8s_deployment.yaml