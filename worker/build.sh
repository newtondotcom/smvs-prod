#!/bin/bash

# Load environment variables from .env file
set -o allexport
source .env
set +o allexport

# Ensure required variables are set
if [[ -z "$DOCKER_REGISTRY" || -z "$DOCKER_USERNAME" || -z "$DOCKER_PASSWORD" || -z "$IMAGE_WORKER_NAME" || -z "$IMAGE_WORKER_TAG" ]]; then
    echo "Error: Required environment variables not set."
    exit 1
fi


# Log in to the Docker registry
echo "Logging in to Docker registry..."
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin "$DOCKER_REGISTRY"

# Build the Docker image for the specified platform
echo "Building Docker image for $TARGET_PLATFORM platform..."
docker buildx create --use
docker buildx build \
    --platform "$TARGET_PLATFORM" \
    -t "$IMAGE_WORKER_NAME:$IMAGE_WORKER_TAG" \
    --secret id=.env,src=.env
    worker/

# Tag the Docker image
echo "Tagging Docker image..."
docker tag "$IMAGE_WORKER_NAME:$IMAGE_WORKER_TAG" "$DOCKER_REGISTRY/$IMAGE_WORKER_NAME:$IMAGE_WORKER_TAG"

# Push the Docker image to the registry
echo "Pushing Docker image to registry..."
docker push "$DOCKER_REGISTRY/$IMAGE_WORKER_NAME:$IMAGE_WORKER_TAG"

# Log out of the Docker registry
echo "Logging out of Docker registry..."
docker logout "$DOCKER_REGISTRY"

echo "Docker tasks completed successfully."