#!/bin/bash

# Example usage:
# ./run_docker.sh 8080 false
# ./run_docker.sh 8081 true

if [ -z "$1" ]; then
    this_port=8501
else
    this_port=$1
fi

if [ -z "$2" ]; then
    rebuild_image=false
else
    rebuild_image=true
fi


if [ -z "$existing_image" ]; then
    docker build . --tag 'ai-toolbox'
else
    echo "Image 'ai-toolbox' already exists."
    if [ "$rebuild_image" = true ]; then
        echo "Rebuilding image 'ai-toolbox'..."
        docker build . --tag 'ai-toolbox'
    fi
fi


existing_container=$(docker ps -aqf "name=ai-toolbox")
docker container kill $existing_container; docker container rm $existing_container
docker run -d -p $this_port:8501  --name ai-toolbox ai-toolbox

# sleep 2 && open http://localhost:8501
