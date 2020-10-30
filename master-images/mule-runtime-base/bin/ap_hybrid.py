#!/usr/bin/env python3
"""
Created on Jun - 2020
@author: David Cisneros
Common functions to access Anypoint Platform ARM/Hybrid APIs
"""
import requests
import json
import os
import subprocess
import logging
import time
import shortuuid
import random
import ap_common

logging.basicConfig(level=logging.INFO)

anypoint_platform_base_url = "https://anypoint.mulesoft.com"

def generate_server_name(server_name):
    final_server_name = server_name
    if not server_name:
        final_server_name = "worker-" + shortuuid.ShortUUID().random(length=7)
    print(final_server_name)
    return final_server_name

# Function to obtain the AMC registration token to register Mule Runtimes in ARM
def get_amc_token(access_token, org_id, env_id):
    complete_url = anypoint_platform_base_url + "/hybrid/api/v1/servers/registrationToken"
    logging.info("Get AMC token - Request: {}".format(complete_url))
    response = requests.get(url = complete_url, headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token, 'X-ANYPNT-ORG-ID': org_id, 'X-ANYPNT-ENV-ID': env_id})
    logging.info("Get AMC token - Received status code: {}".format(response.status_code))
    amc_token = None
    if response.status_code == 200:
        amc_token = response.json()['data']
        logging.info("Get AMC token - Response: {}".format(amc_token))
    else:
        logging.info("Get AMC token - Response: failed: {}".format(str(response.status_code)))
    
    print(amc_token)
    return amc_token

# Function to get the server id based on the server name
def get_server_id(access_token, org_id, env_id, server_name):
    complete_url = anypoint_platform_base_url + "/hybrid/api/v1/servers"
    logging.info("Get Server id - Request: {}".format(complete_url))
    response = requests.get(url = complete_url, headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token, 'X-ANYPNT-ORG-ID': org_id, 'X-ANYPNT-ENV-ID': env_id})
    logging.info("Get Server id - Received status code: {}".format(response.status_code))
    server_id = None
    if response.status_code == 200:
        servers_list = response.json()['data']
        for server in servers_list:
            if (server['name'].lower() == server_name.lower()):
                server_id = server['id']
                logging.info("Get Server id - Response: {}".format(server_id))
                break
    else:
        logging.info("Get Server id - Response: failed: {}".format(str(response.status_code)))
    
    if not server_id:
        logging.info("Get Server id - Response: Server name not found")

    print(server_id)
    return server_id

# Function to get the serverGroup id based on the server name
def get_server_group_id_from_server(access_token, org_id, env_id, server_id):
    complete_url = anypoint_platform_base_url + "/hybrid/api/v1/servers/" + str(server_id) 
    logging.info("Get ServerGroup id from server - Request: {}".format(complete_url))
    response = requests.get(url = complete_url, headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token, 'X-ANYPNT-ORG-ID': org_id, 'X-ANYPNT-ENV-ID': env_id})
    logging.info("Get ServerGroup id from server - Received status code: {}".format(response.status_code))
    server_group_id = None
    if response.status_code == 200:
        server_group_id = response.json()['data']['serverGroupId']
        logging.info("Get ServerGroup id from server - ServerGroupId: {}".format(server_group_id))
    else:
        logging.info("Get ServerGroup id from server - Response: failed: {}".format(str(response.status_code)))
    
    if not server_group_id:
        logging.info("Get ServerGroup id from server - Response: Server name not found")

    print(server_group_id)
    return server_group_id

# Function to get the server id based on the server name
def get_server_status(access_token, org_id, env_id, server_name):
    complete_url = anypoint_platform_base_url + "/hybrid/api/v1/servers"
    logging.info("Get Server status - Request: {}".format(complete_url))
    response = requests.get(url = complete_url, headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token, 'X-ANYPNT-ORG-ID': org_id, 'X-ANYPNT-ENV-ID': env_id})
    logging.info("Get Server status - Received status code: {}".format(response.status_code))
    server_status = None
    if response.status_code == 200:
        servers_list = response.json()['data']
        for server in servers_list:
            if (server['name'].lower() == server_name.lower()):
                server_status = server['status']
                logging.info("Get Server status - Response: {}".format(server_status))
                break
    else:
        logging.info("Get Server status - Response: failed: {}".format(str(response.status_code)))

    if not server_status:
        logging.info("Get Server status - Response: Server name not found")
    
    print(server_status)
    return server_status


# Function to get the server group id based on the server group name
def get_server_group_id(access_token, org_id, env_id, server_group_name):
    complete_url = anypoint_platform_base_url + "/hybrid/api/v1/serverGroups"
    logging.info("Get Server Group id - Request: {}".format(complete_url))
    response = requests.get(url = complete_url, headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token, 'X-ANYPNT-ORG-ID': org_id, 'X-ANYPNT-ENV-ID': env_id})
    logging.info("Get Server Group id - Received status code: {}".format(response.status_code))
    server_group_id = None
    if response.status_code == 200:
        server_groups_list = response.json()['data']
        for server_group in server_groups_list:
            if (server_group['name'].lower() == server_group_name.lower()):
                server_group_id = server_group['id']
                logging.info("Get Server Group id - Response: {}".format(server_group_id))
                break
    else:
        logging.info("Get Server Group id - Response: failed: {}".format(str(response.status_code)))
    
    if not server_group_id:
        logging.info("Get Server Group id - Response: Server Group name not found")

    print(server_group_id)
    return server_group_id

# Function to get the servers from a server group name
def get_server_group_servers(access_token, org_id, env_id, server_group_id):
    complete_url = anypoint_platform_base_url + "/hybrid/api/v1/serverGroups/" + str(server_group_id) 
    logging.info("Get Servers from Server Group - Request: {}".format(complete_url))
    response = requests.get(url = complete_url, headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token, 'X-ANYPNT-ORG-ID': org_id, 'X-ANYPNT-ENV-ID': env_id})
    logging.info("Get Servers from Server Group - Received status code: {}".format(response.status_code))
    servers = None
    if response.status_code == 200:
        server_groups_list = response.json()['data']
        servers = server_groups_list['servers']
        logging.info("Get Servers from Server Group - Response: {}".format(servers))
    else:
        logging.info("Get Servers from Server Group - Response: failed: {}".format(str(response.status_code)))
    
    if not servers:
        logging.info("Get Servers from Server Group - Response: Servers not found")

    print(servers)
    return servers


# Function to create a serverGroup 
def create_server_group(access_token, org_id, env_id, server_group_name):
    complete_url = anypoint_platform_base_url + "/hybrid/api/v1/serverGroups"
    logging.info("Create Server Group - Request: {}".format(complete_url))
    payload = json.dumps({'name': server_group_name, 'serverIds': [] })
    response = requests.post(url = complete_url, data = payload, headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token, 'X-ANYPNT-ORG-ID': org_id, 'X-ANYPNT-ENV-ID': env_id})
    logging.info("Create Server Group - Received status code: {}".format(response.status_code))
    
    if response.status_code == 200:
        logging.info("Create Server Group - Response: {}".format(response.text))
    else:
        logging.info("Create Server Group - Response: failed: {}".format(str(response.status_code)))


# Function to add a server to a server Group 
def add_server_to_server_group(access_token, org_id, env_id, server_group_id, server_id):
    complete_url = anypoint_platform_base_url + "/hybrid/api/v1/serverGroups/" + str(server_group_id) + "/servers/" + str(server_id)
    logging.info("Add server to Server Group - Request: {}".format(complete_url))
    response = requests.post(url = complete_url, headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token, 'X-ANYPNT-ORG-ID': org_id, 'X-ANYPNT-ENV-ID': env_id})
    logging.info("Add server to Server Group - Received status code: {}".format(response.status_code))
    if response.status_code == 200 or response.status_code == 202:
        logging.info("Add server to Server Group - Response: {}".format(response.text))
    else:
        logging.info("Add server to Server Group - Response: failed: {}".format(str(response.status_code)))


# Function to remove a server from a server Group 
def remove_server_from_server_group(access_token, org_id, env_id, server_group_id, server_id):
    complete_url = anypoint_platform_base_url + "/hybrid/api/v1/serverGroups/" + str(server_group_id) + "/servers/" + str(server_id)
    logging.info("Remove server from Server Group - Request: {}".format(complete_url))
    response = requests.delete(url = complete_url, headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token, 'X-ANYPNT-ORG-ID': org_id, 'X-ANYPNT-ENV-ID': env_id})
    logging.info("Remove server from Server Group - Received status code: {}".format(response.status_code))
    if response.status_code == 200 or response.status_code == 202 or response.status_code == 204:
        logging.info("Remove server from Server Group - Response: {}".format(response.text))
    else:
        logging.info("Remove server from Server Group - Response: failed: {}".format(str(response.status_code)))


# Function to remove a Server Group 
def remove_server_group(access_token, org_id, env_id, server_group_id, server_id):
    complete_url = anypoint_platform_base_url + "/hybrid/api/v1/serverGroups/" + str(server_group_id)
    logging.info("Remove Server Group - Request: {}".format(complete_url))
    response = requests.delete(url = complete_url, headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token, 'X-ANYPNT-ORG-ID': org_id, 'X-ANYPNT-ENV-ID': env_id})
    logging.info("Remove Server Group - Received status code: {}".format(response.status_code))
    if response.status_code == 200 or response.status_code == 202 or response.status_code == 204:
        logging.info("Remove Server Group - Response: {}".format(response.text))
    else:
        logging.info("Remove Server Group - Response: failed: {}".format(str(response.status_code)))

# Function to remove a Server  
def remove_server(access_token, org_id, env_id, server_id):
    complete_url = anypoint_platform_base_url + "/hybrid/api/v1/servers/" + str(server_id)
    logging.info("Remove Server - Request: {}".format(complete_url))
    response = requests.delete(url = complete_url, headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token, 'X-ANYPNT-ORG-ID': org_id, 'X-ANYPNT-ENV-ID': env_id})
    logging.info("Remove Server - Received status code: {}".format(response.status_code))
    if response.status_code == 200 or response.status_code == 202 or response.status_code == 204:
        logging.info("Remove Server - Response: {}".format(response.text))
    else:
        logging.info("Remove Server - Response: failed: {}".format(str(response.status_code)))

# Function to identify if the server group was already created with the specified name
def is_server_group_registered(access_token, org_id, env_id, server_group_name):
    
    exist = false
    server_group_id = get_server_group_id(access_token, org_id, env_id, server_group_name)
    if server_group_id == None:
        logging.info("Server group does not exist")
    else:
         logging.info("Server group does exist")
         exist = true

    return exist

# Function to create or extend server group
def verify_and_create_or_extend_server_group(access_token, org_id, env_id, server_name, target_type, target_name, application_name):
    
    if target_type == "server":
        logging.info("Verify Server Groups - Target type 'server', server group verification is not needed")
    else:
        server_id = get_server_id(access_token, org_id, env_id, server_name)
        if server_id == None:
            logging.info("Verify Server Groups - Server Id not found") 
        else:
            logging.info("Verify Server Groups - Target type 'serverGroup', server group verification is needed")    
            server_group_id = get_server_group_id(access_token, org_id, env_id, target_name)
            if server_group_id == None:
                logging.info("Verify Server Groups - Server group doesn't exist, Creating a new server group and adding the server to it")
                create_server_group(access_token, org_id, env_id, target_name)
                time.sleep(5)
                server_group_id = get_server_group_id(access_token, org_id, env_id, target_name)
                add_server_to_server_group(access_token, org_id, env_id, server_group_id, server_id)
            else:
                logging.info("Verify Server Groups - Server group exists, removing application (optional) before adding the server to the serverGroup")
                # Undedploying the application is not necessary, doing it generates problem with the AM-agent for application metrics, a redeployment is enough
                #application_id = get_application_id(access_token, org_id, env_id, server_group_id, application_name)
                #remove_application(access_token, org_id, env_id, application_id)
                time.sleep(5)
                add_server_to_server_group(access_token, org_id, env_id, server_group_id, server_id)

# Function to clean un server and server group
def clean_up_server_and_server_group(access_token, org_id, env_id, server_id, target_type, target_name):
    
    if target_type == "server":
        logging.info("Clean up server and server groups - Target type server")
        logging.info("Clean up server and server groups - Remove server")
        remove_server(access_token, org_id, env_id, server_id)
    else:
        logging.info("Clean up server and server groups - Target type serverGroup")
        server_group_id = get_server_group_id_from_server(access_token, org_id, env_id, server_id)
        if server_group_id != None:
            logging.info("Clean up server and server groups - ServerGroupId found in server")
            remove_server_from_server_group(access_token, org_id, env_id, server_group_id, server_id)
            remove_server(access_token, org_id, env_id, server_id)
            servers = get_server_group_servers(access_token, org_id, env_id, server_group_id)
            if len(servers) == 0:
                logging.info("Clean up server and server groups - ServerGroup is empty, removing it")
                remove_server_group(access_token, org_id, env_id, server_group_id, server_id)
            else:
                logging.info("Clean up server and server groups - ServerGroup is not empty")
        else:
            logging.info("Clean up server and server groups - ServerGroupId not found in server")


def wait_server_status(access_token, org_id, env_id, server_name, expected_status, wait_time):
    server_status = get_server_status(access_token, org_id, env_id, server_name)
    logging.info("Wait server status - current: {}".format(server_status))
    while server_status != expected_status:
        time.sleep(wait_time)
        server_status = get_server_status(access_token, org_id, env_id, server_name)

def wait_application_status(access_token, org_id, env_id, target_type, server_name, server_group_name, application_name, expected_status, wait_time):
    if target_type == "server":
        target_id = get_server_id(access_token, org_id, env_id, server_name)
    else:
        target_id = get_server_group_id(access_token, org_id, env_id, server_group_name)

    application_status = get_application_status(access_token, org_id, env_id, target_id, application_name)
    logging.info("Wait application status - current: {}".format(application_status))
    while application_status != expected_status:
        time.sleep(wait_time)
        application_status = get_application_status(access_token, org_id, env_id, target_id, application_name)

def verify_and_deploy_application(access_token, org_id, env_id, target_type, server_name, server_group_name, artifact_name, file_path, properties={}):
    if target_type == "server":
        logging.info("Verify Deploy - Deploying to a server")
        target_id = get_server_id(access_token, org_id, env_id, server_name)
        deploy_application(access_token, org_id, env_id, target_id, artifact_name, file_path, properties)
    else:
        logging.info("Verify Deploy - Deploying to a serverGroup")
        target_id = get_server_group_id(access_token, org_id, env_id, server_group_name)
        deploy_application(access_token, org_id, env_id, target_id, artifact_name, file_path, properties)

# Function to deploy an Application
def deploy_application(access_token, org_id, env_id, target_id, artifact_name, file_path, properties={}):
    complete_url = anypoint_platform_base_url + "/hybrid/api/v1/applications"
    logging.info("Deploy application - Request: {}".format(complete_url))
    logging.info("Deploy application - Properties Received: {}".format(properties))

    file_binary = open(file_path, 'rb')
    complete_configuration = None
    if not properties:
        complete_configuration = json.dumps({})
    else:
        complete_configuration = json.dumps({"mule.agent.application.properties.service": {"applicationName": artifact_name,"properties": properties }}) 

    logging.info("Deploy application - Properties Configuration: {}".format(complete_configuration))
    multipart_form_data = {
        'file': (file_path, file_binary),
        'artifactName': ( None, artifact_name ),
        'targetId': ( None, target_id),
        'configuration': (None, complete_configuration)
    }

    response = requests.post(url = complete_url, files = multipart_form_data, headers = {'Authorization': 'Bearer ' + access_token, 'X-ANYPNT-ORG-ID': org_id, 'X-ANYPNT-ENV-ID': env_id})
    logging.info("Deploy application - Received status code: {}".format(response.status_code))
    if response.status_code == 200 or response.status_code == 201 or response.status_code == 202:
        logging.info("Deploy application - Response: {}".format(response.text))
    else:
        logging.info("Deploy application - Response: failed: {}".format(str(response.status_code)))
        logging.error("Deploy application - Response: failed: {}".format(response.text))


# Function to remove an Application
def remove_application(access_token, org_id, env_id, application_id):
    complete_url = anypoint_platform_base_url + "/hybrid/api/v1/applications/" + str(application_id)
    logging.info("Remove Application - Request: {}".format(complete_url))
    response = requests.delete(url = complete_url, headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token, 'X-ANYPNT-ORG-ID': org_id, 'X-ANYPNT-ENV-ID': env_id})
    logging.info("Remove Application - Received status code: {}".format(response.status_code))
    if response.status_code == 200 or response.status_code == 202 or response.status_code == 204:
        logging.info("Remove Application - Response: {}".format(response.text))
    else:
        logging.info("Remove Application - Response: failed: {}".format(str(response.status_code)))


# Function to get the application id based on the target id and application name
def get_application_id(access_token, org_id, env_id, target_id, application_name):
    complete_url = anypoint_platform_base_url + "/hybrid/api/v1/applications?targetId=" + str(target_id) 
    logging.info("Get Application id - Request: {}".format(complete_url))
    response = requests.get(url = complete_url, headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token, 'X-ANYPNT-ORG-ID': org_id, 'X-ANYPNT-ENV-ID': env_id})
    logging.info("Get Application id - Received status code: {}".format(response.status_code))
    application_id = None
    if response.status_code == 200:
        applications_data = response.json()['data']
        for app_data in applications_data:
            if (app_data['name'].lower() == application_name.lower()):
                artifacts_data = app_data['serverArtifacts']
                for artifact_data in artifacts_data:
                    application_id = artifact_data['deploymentId']
                    logging.info("Get Application id - Response: {}".format(application_id))
                    break
    else:
        logging.info("Get Application id - Response: failed: {}".format(str(response.status_code)))
    
    if not application_id:
        logging.info("Get Application id - Response: Server Group name not found")

    print(application_id)
    return application_id

# Function to get the application status based on the target id and application name
def get_application_status(access_token, org_id, env_id, target_id, application_name):
    complete_url = anypoint_platform_base_url + "/hybrid/api/v1/applications?targetId=" + str(target_id) 
    logging.info("Get Application status - Request: {}".format(complete_url))
    response = requests.get(url = complete_url, headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token, 'X-ANYPNT-ORG-ID': org_id, 'X-ANYPNT-ENV-ID': env_id})
    logging.info("Get Application status - Received status code: {}".format(response.status_code))
    application_status = None
    if response.status_code == 200:
        applications_data = response.json()['data']
        for app_data in applications_data:
            if (app_data['name'].lower() == application_name.lower()):
                artifacts_data = app_data['serverArtifacts']
                for artifact_data in artifacts_data:
                    application_status = artifact_data['lastReportedStatus']
                    logging.info("Get Application status - Response: {}".format(application_status))
                    break
    else:
        logging.info("Get Application status - Response: failed: {}".format(str(response.status_code)))
    
    if not application_status:
        logging.info("Get Application status - Response: Application status not found")

    print(application_status)
    return application_status
