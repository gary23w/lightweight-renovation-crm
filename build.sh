#!/bin/bash
set -e  # stop on error

CONTAINER_NAME="backend_api_1"
IMAGE_NAME="backend_api"

# Function to check if a command succeeded
function check_success {
    if [ $? -ne 0 ]; then
        echo "Error encountered. Exiting..."
        exit 1
    fi
}

# Remove old docker container
if docker container inspect $CONTAINER_NAME > /dev/null 2>&1; then
    echo "Removing old Docker container..."
    docker container rm -f $CONTAINER_NAME
    check_success
else
    echo "No existing Docker container found. Continuing..."
fi

# Remove old docker image
if docker image inspect $IMAGE_NAME > /dev/null 2>&1; then
    echo "Removing old Docker image..."
    docker image rm -f $IMAGE_NAME
    check_success
else
    echo "No existing Docker image found. Continuing..."
fi

# Build and start new docker containers
echo "Starting new Docker containers..."
docker-compose up -d
check_success

echo "[+] Done!!! You can now access the REST API at http://localhost:8080/"
