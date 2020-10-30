#!/bin/bash

NEXUS_USER='xxxxxxxxx'
NEXUS_PASS='xxxxxxxxx'

DOCKER_PREFIX='metrics'
APP='test-app'
CURRENT=`pwd`
APP_FOLDER="$CURRENT/$APP"
BASE_IMG_FOLDER="$CURRENT/master-images/ubuntu-enriched-base"
RUNTIME_IMG_FOLDER="$CURRENT/master-images/mule-runtime-base"
TAG='latest'

RUNTIME_VERSION=4.3.0

#BUILD UBUNTU ENRICHED IMAGE
cd $BASE_IMG_FOLDER
docker build -t "$DOCKER_PREFIX/ubuntu-enriched:$TAG" .

#BUILD RUNTIME USING UBUNTU
cd $RUNTIME_IMG_FOLDER
docker build \
  --build-arg BASE_IMAGE="$DOCKER_PREFIX/ubuntu-enriched:$TAG" \
  --build-arg NEXUS_USER=$NEXUS_USER \
  --build-arg NEXUS_PASS=$NEXUS_PASS \
  --build-arg MULE_VERSION=$RUNTIME_VERSION \
  -t "$DOCKER_PREFIX/mule-runtime-$RUNTIME_VERSION:$TAG" .

cd $CURRENT

