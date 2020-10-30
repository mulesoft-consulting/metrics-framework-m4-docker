###############################################################################
## Ubuntu image enriched with tools like java (open jdk), jq, maven, etc
## Version:  1.0
## Based on:  ubuntu:latest
###############################################################################

ARG                     BASE_IMAGE=ubuntu:latest
FROM                    $BASE_IMAGE
MAINTAINER              David Cisneros <david.cisneros@mulesoft.com>

###############################################################################
## Setting up arguments

ARG 	DEBIAN_FRONTEND=noninteractive

ARG     TZ=America/Los_Angeles

###############################################################################
## Base container configurations

# Install base pre-requisites (openjdk, curl, jq, maven, os updates), purge apt lists and configure instance timezone
RUN     apt-get update && \
        apt-get install -y --no-install-recommends \
        apt-utils \
        curl \
        jq \
        maven \
        gnupg2 \
        sudo \
        tzdata \
        wget \
        unzip \
        net-tools \
        netcat \
        iputils-ping \
        dnsutils \
        iproute2 \
        lsof \
        openssl \
        python3.8 \
        python3-pip \
        openjdk-8-jdk \
        && pip3 install requests \
        && pip3 install shortuuid \
        && update-java-alternatives --set  /usr/lib/jvm/java-1.8.0-openjdk-amd64 \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* \
        && echo "$TZ" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata

