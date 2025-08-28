#! /bin/bash

REPO_NAME="permitta"
IMAGE_NAME="permitta-core"
IMAGE_TAG=$(cat version.txt)
BUILD_CONTEXT="."

if command -v podman &> /dev/null; then
    CONTAINER_ENGINE="podman"
elif command -v docker &> /dev/null; then
    CONTAINER_ENGINE="docker"
else
    echo "Error: Neither Docker nor Podman found"
    exit 1
fi

echo "Building version $REPO_NAME/$IMAGE_NAME:$IMAGE_TAG with $CONTAINER_ENGINE"
$CONTAINER_ENGINE build -t $REPO_NAME/$IMAGE_NAME:$IMAGE_TAG $BUILD_CONTEXT