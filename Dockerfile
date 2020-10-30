###############################################################################
## Dockerizing Mule Runtime Enterprise Edition with one Application
## Version:  1.0
## Based on:  mule-runtime-4.3.0:latest  from master-images
###############################################################################


ARG                     BASE_RUNTIME_IMAGE=mule-runtime:4.3.0
FROM                    $BASE_RUNTIME_IMAGE

###############################################################################
## Setting up arguments

ARG     MULE_PATH=/opt/mule/bin/

ARG     APP_NAME
ARG     APP_PATH=/opt/mule/apps/

ENV     ANYPOINT_USERNAME= \
	ANYPOINT_PASSWORD= \
        ANYPOINT_ORG_NAME= \
        ANYPOINT_ENV_NAME= \
        SERVER_NAME= \
        TARGET_TYPE=server \
        TARGET_NAME=$APP_NAME-server-group 

#USER mule

###############################################################################
## Copy Mule Application 

#RUN         mkdir $APP_PATH

#Copy the jar (the build should have happened before building the app image)
COPY        ./target/*.jar $APP_PATH

###############################################################################
## Expose ports for the application

EXPOSE 8081 

###############################################################################
## Environment and execution

ENV             MULE_BASE /opt/mule
WORKDIR         $MULE_PATH
ENTRYPOINT      ["/opt/mule/bin/docker-entrypoint.sh"]
