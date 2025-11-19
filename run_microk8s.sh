#!/bin/bash


docker build . -t localhost:32000/ai-toolbox:registry

microk8s kubectl apply -f nginx.yaml