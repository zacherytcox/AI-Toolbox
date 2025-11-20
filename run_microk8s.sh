#!/bin/bash


docker build . -t localhost:32000/ai-toolbox:latest

docker push localhost:32000/ai-toolbox

# microk8s ctr image pull microk8s-1:32000/ai-toolbox:latest
# microk8s kubectl create deployment nginx --image=10.141.241.175:32000/mynginx:registry
# microk8s images import microk8s-1:32000/ai-toolbox:latest

MANIFEST=microk8s_deployment.yaml
DEPLOYMENT=ai-toolbox

out=$(microk8s kubectl apply -f "$MANIFEST")
echo "$out"

# If apply didn't create or configure anything (i.e. everything was "unchanged"),
# then force a rollout restart so pods get recreated.
if ! grep -qE ' (created|configured|patched)' <<< "$out"; then
  echo "No spec changes detected, forcing rollout restart..."
  microk8s kubectl rollout restart deployment "$DEPLOYMENT"
fi


# microk8s kubectl apply -f microk8s_deployment.yaml