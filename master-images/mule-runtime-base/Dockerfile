###############################################################################
## Dockerizing Mule Runtime Enterprise Edition
## Version:  1.0
## Based on:  ubuntu-enriched:1.0.0 from master-images
###############################################################################

ARG                     BASE_IMAGE=ubuntu-enriched:1.0.0
FROM                    $BASE_IMAGE
MAINTAINER              David Cisneros <david.cisneros@mulesoft.com>

###############################################################################
## Setting up arguments

ARG     MULESOFT_NEXUS_EE_URL=repository.mulesoft.org/nexus/content/repositories/releases-ee
ARG     ANYPOINT_CDN_URL=https://s3.amazonaws.com/cdn-anypoint-prod/artifacts

ARG     MULE_VERSION=4.2.2
ARG     MULE_RUNTIME_DISTRIBUTION=mule-ee-distribution-standalone-$MULE_VERSION.tar.gz
ARG     MULE_HOME=/opt/mule-enterprise-standalone-$MULE_VERSION

ARG     AM_AGENT_VERSION=2.2.3.0
ARG     AM_AGENT_DISTRIBUTION=am-$AM_AGENT_VERSION.zip

ARG     MULE_AGENT_VERSION=2.4.6
ARG     MULE_AGENT_DISTRIBUTION=agent-setup-$MULE_AGENT_VERSION.zip

ARG 	DEBIAN_FRONTEND=noninteractive

ARG     NEXUS_USER
ARG     NEXUS_PASS

ARG     ASSETS_DIR=./bin
ARG     MULE_PATH=/opt/mule/bin/

ENV     MAX_RAM=1g 

###############################################################################
## MuleEE installation

## Download distribution, unzip it, create a sym link, create Mule user and change permissions
WORKDIR /opt/

RUN wget -q --show-progress --progress=bar:force https://$NEXUS_USER:$NEXUS_PASS@$MULESOFT_NEXUS_EE_URL/com/mulesoft/mule/distributions/mule-ee-distribution-standalone/$MULE_VERSION/$MULE_RUNTIME_DISTRIBUTION 2>&1 \
    &&  tar -xzvf /opt/$MULE_RUNTIME_DISTRIBUTION \
    &&  ls \
    &&  ln -s $MULE_HOME/ mule \
    &&  ls -l mule \
    &&  rm -f $MULE_RUNTIME_DISTRIBUTION  

## Remove files and examples that are not needed - Not needed anymore, the mmc jars, examples and default apps were removed from the distribution > 4.2.1

## Download latest Mule Agent - do not execute the update script, the mule-agent.yml file needs to be available (after the Runtime registration)
RUN wget -q --show-progress --progress=bar:force https://$NEXUS_USER:$NEXUS_PASS@$MULESOFT_NEXUS_EE_URL/com/mulesoft/agent/agent-setup/$MULE_AGENT_VERSION/$MULE_AGENT_DISTRIBUTION 2>&1 \
    && unzip -o $MULE_AGENT_DISTRIBUTION -d $MULE_HOME/bin \
    && rm -f $MULE_AGENT_DISTRIBUTION

## Download Monitoring agent - do not execute the install script, the mule-agent.yml file needs to be available (after the Runtime registration)
RUN wget -q --show-progress --progress=bar:force $ANYPOINT_CDN_URL/monitoring-center-ui/app/hybrid/$AM_AGENT_DISTRIBUTION 2>&1 \
	&& unzip $AM_AGENT_DISTRIBUTION -d $MULE_HOME \
	&& rm -f $AM_AGENT_DISTRIBUTION

## Copy the License file - pre-package into docker image to avoid leakage
COPY  ./license.lic /opt/mule/conf/
RUN   /opt/mule/bin/mule -installLicense /opt/mule/conf/license.lic
RUN   rm -f /opt/mule/conf/license.lic

## Include additional wrapper configurations
COPY ./wrapper-docker.conf /opt/mule/conf
RUN  echo '#include.required /opt/mule/conf/wrapper-docker.conf' >> /opt/mule/conf/wrapper.conf
RUN  sed -i '/XX\:\(Max\)\{0,1\}NewSize/d' /opt/mule/conf/wrapper.conf && \
     sed -i '/XX\:\(Max\)\{0,1\}PermSize/d' /opt/mule/conf/wrapper.conf

## Include partial patches - full module patches, plugin and services patches are not included since the process is more complex and trying to automate it can break the image portability  
COPY ./patches /opt/mule/lib/patches


###############################################################################
## Copy Mule Runtime startup scripts

COPY     $ASSETS_DIR/docker-entrypoint.sh $ASSETS_DIR/ap_common.py $ASSETS_DIR/ap_hybrid.py $MULE_PATH
RUN     chmod 755 ${MULE_PATH}docker-entrypoint.sh \
        ${MULE_PATH}ap_common.py \
        ${MULE_PATH}ap_hybrid.py

###############################################################################
## Add user and change ownership of the MULE_HOME
#RUN useradd -ms /bin/bash mule \
#    && chown -R mule:mule $MULE_HOME 

#RUN mkdir /opt/mule/.mule \
#    && adduser --disabled-password --gecos '' mule \
#    && adduser mule sudo \
#    && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
#    && echo 'mule ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
#    && chown -R mule:mule $MULE_HOME 

###############################################################################

## Expose ports for the cluster communication, remote debugger and JMX
#Commented for now since cluster features are not used and JMX and remote debugger are not needed
#EXPOSE 5000 1098 5701 54327 

###############################################################################
## Define volumes

VOLUME ["/opt/mule/logs", "/opt/mule/conf", "/opt/mule/apps", "/opt/mule/domains","/opt/mule/.mule","/opt/mule/patches"]
