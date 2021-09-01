#!/usr/bin/env bash

set -e

echo "Building docker image.."

bazel run -c opt //cisei:cisei_image -- --norun

echo "Docker image built successfully!"

IMG_TAG="latest"

echo "Pushing docker image.."

bazel run -c opt --define image_tag="${IMG_TAG}" //cisei:push_cisei_image

echo "Docker image pushed successfully!"
