#!/bin/bash

username=${ANYPOINT_USERNAME}
password=${ANYPOINT_PASSWORD}
org_name=${ANYPOINT_ORG_NAME}
env_name=${ANYPOINT_ENV_NAME}
target_name=${TARGET_NAME}
application_name=${APP_NAME}
application_props=${APP_PROPS}
target_type=${TARGET_TYPE}

mule_base_path="/opt/mule"
pid=0

# SIGTERM-handler
term_handler() {
  echo "SIGTERM handler called pid: $pid, last process $!"

  if [ $pid -ne 0 ]; then
  	echo 'PID not null, killing pid'
    kill -SIGTERM "$pid"
    echo 'Waiting for pid to be killed'
    wait "$pid"
  fi

  echo 'Performing clean up actions from the SIGTERM Handler'
  perform_cleanup

  exit 143; # 128 + 15 -- SIGTERM
}

# SIGKILL-handler
kill_handler() {
  echo "SIGKILL handler just for reference, SIGTERM is called first, always"
}

perform_cleanup() {
	echo 'Getting access token'
	access_token=$(python3 -c "import ap_common; ap_common.get_access_token('$username', '$password')")
	echo '--------'
	echo $token

	echo 'Clean up server and server group'
	access_token=$(python3 -c "import ap_hybrid; ap_hybrid.clean_up_server_and_server_group('$access_token', '$org_id', '$env_id', '$server_id', '$target_type', '$target_name')")
	echo '--------'
	echo $token
}

# sleep time
wait_server_status() {
    server_status=$(python3 -c "import ap_hybrid; ap_hybrid.get_server_status('$access_token', '$org_id', '$env_id', '$server_name')")
    max_attempts=10
    counter=0
    echo "Server status obtained: $server_status"
    while [ "$server_status" != "RUNNING" ]
    do
        echo "Server status counter: $counter"
        sleep $1
        server_status=$(python3 -c "import ap_hybrid; ap_hybrid.get_server_status('$access_token', '$org_id', '$env_id', '$server_name')")
        counter=$((counter+1))
        if [ "$counter" == "$max_attempts" ]
          then
            echo "Obtaining server status after $max_attempts attempts failed, clean and exit the container"
            perform_cleanup
            exit 2
        fi
    done
}

# sleep time
wait_application_status() {

    if [ "target_type" == "server" ]
        then
            local_target_id=$server_id

        else
            local_target_id=$server_group_id
    fi

    application_status=$(python3 -c "import ap_hybrid; ap_hybrid.get_application_status('$access_token', '$org_id', '$env_id', '$local_target_id', '$application_name')")
    echo "Application status obtained: $application_status"
    while [ "$application_status" != "STARTED" ]
    do
    	if [ "$application_status" == "DEPLOYMENT_FAILED" ]
    		then
    			echo 'Deployment failed, clean and exit the container'
    			perform_cleanup
				  exit 2
    	fi
        sleep $1
        application_status=$(python3 -c "import ap_hybrid; ap_hybrid.get_application_status('$access_token', '$org_id', '$env_id', '$local_target_id', '$application_name')")
    done
}

echo 'Verifying server name'
server_name=$(python3 -c "import ap_hybrid; ap_hybrid.generate_server_name('${SERVER_NAME}')")
if [ "$server_name" == "None" ] || [ -z "$server_name" ]
then
	echo 'Error getting the server name'
	exit 2
else 
	echo '--------'
	echo $server_name
fi

echo 'Getting access token'
access_token=$(python3 -c "import ap_common; ap_common.get_access_token('$username', '$password')")
if [ "$access_token" == "None" ] || [ -z "$access_token" ]
then
	echo 'Error getting the token'
	exit 2
else 
	echo '--------'
	echo $token
fi


echo 'Getting organization Id'
org_id=$(python3 -c "import ap_common; ap_common.get_organization_id('$access_token', '$org_name')")
if [ "$org_id" == "None" ] || [ -z "$org_id" ]
then
	echo 'Error getting the organization id'
	exit 2
else
	echo '--------'
	echo $org_id
fi

echo 'Getting environment Id'
env_id=$(python3 -c "import ap_common; ap_common.get_environment_id('$access_token', '$org_id', '$env_name')")
if [ "$env_id" == "None" ] || [ -z "$env_id" ]
then
	echo 'Error getting the environment id'
	exit 2
else
	echo '--------'
	echo $env_id
fi

echo 'Getting ACM registration token'
amc_token=$(python3 -c "import ap_hybrid; ap_hybrid.get_amc_token('$access_token', '$org_id', '$env_id')")
if [ "$amc_token" == "None" ] || [ -z "$amc_token" ]
then
	echo 'Error getting the ACM token id'
	exit 2
else	
	echo '--------'
	echo $amc_token
fi

echo 'Registering server'
$mule_base_path/bin/amc_setup -H $amc_token $server_name
echo '--------'

echo 'Updating Mule Agent'
$mule_base_path/bin/amc_setup -U
echo '--------'

echo 'Installing Monitoring Agent'
$mule_base_path/am/bin/install -x Y
echo '--------'
 
echo 'Starting Mule process in backgroud to setup Anypoint Monitoring agent'
./mule start
echo '--------'

echo 'Waiting for server status to be RUNNING'
wait_server_status 10
echo '--------'

echo 'Setting up Anypoint Monitoring agent'
$mule_base_path/am/bin/setup
echo '--------'

echo 'Verify and create or extend server group'
tmp=$(python3 -c "import ap_hybrid; ap_hybrid.verify_and_create_or_extend_server_group('$access_token', '$org_id', '$env_id', '$server_name', '$target_type', '$target_name', '$application_name')")
echo '--------'

echo 'Waiting for server status to be RUNNING'
wait_server_status 10
echo '--------'

echo 'Getting server id to be used as part of the clean up'
server_id=$(python3 -c "import ap_hybrid; ap_hybrid.get_server_id('$access_token', '$org_id', '$env_id', '$server_name')")
echo '--------'

if [ "$target_type" == "serverGroup" ]
then
      echo "Target type is serverGroup, getting server group id to update mule-agent"
      server_group_id=$(python3 -c "import ap_hybrid; ap_hybrid.get_server_group_id('$access_token', '$org_id', '$env_id', '$target_name')")
      echo "Server Group id is: $server_group_id"
      sed -i "/^\([[:space:]]*clusterId: \).*/s//\1'$server_group_id'/" /opt/mule/conf/mule-agent.yml
      sed -i "/^\([[:space:]]*worker_id: \).*/s//\1'$server_id'/" /opt/mule/conf/mule-agent.yml  
else
      echo "Target type is server, no need to update mule-agent"
fi

echo 'Stopping the mule process to take mule-agent updates'
./mule stop
echo '--------'

echo 'Starting the Mule process and attaching it to the docker-entrypoint wait'
./mule $WRAPPER_PROPS &
pid="$!"

trap 'kill ${!}; term_handler' SIGTERM
trap 'kill ${!}; kill_handler' SIGKILL

echo 'Waiting for server status to be RUNNING'
wait_server_status 10
echo '--------'

echo 'Verify and deploy'
file_path=$(ls -rt ${mule_base_path}/app_tmp/*.jar | tail -1)
tmp=$(python3 -c "import ap_hybrid; ap_hybrid.verify_and_deploy_application('$access_token', '$org_id', '$env_id', '$target_type', '$server_name', '$target_name', '$application_name', '$file_path', ${application_props})")
echo '--------'

echo 'Waiting for application status to be STARTED'
wait_application_status 10
echo '--------'

echo 'Keeping the mule process up and running'
wait $pid

# wait forever
#while true
#do
#  tail -f /dev/null & wait ${!}
#done

echo 'Performing clean up actions from the end of the docker entrypoint'
perform_cleanup
