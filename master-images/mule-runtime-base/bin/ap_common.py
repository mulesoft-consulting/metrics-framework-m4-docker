#!/usr/bin/env python3
"""
Created on Jun - 2020
@author: David Cisneros
Common functions to access Anypoint Platform APIs
"""
import requests
import json
import os
import logging

logging.basicConfig(level=logging.INFO)

anypoint_platform_base_url = "https://anypoint.mulesoft.com"

# Function to obtain the bearer token to be used in subsequent Anypoint Platform API calls
def get_access_token(username, password):
    complete_url = anypoint_platform_base_url + "/accounts/login/"
    payload = json.dumps({'username': username, 'password': password})
    logging.info("Get access token - Request: {}".format(complete_url))
    response = requests.post(url = complete_url, data = payload, headers = {'Content-type': 'application/json'})
    logging.info("Get access token - Received status code: {}".format(response.status_code))

    access_token = None
    if response.status_code == 200:
        access_token = response.json()['access_token']
        logging.info("Get access token - Response: {}".format(access_token))
    else:
        logging.info("Get access token - Response: failed: {}".format(str(response.status_code))) 
    print(access_token) 
    return access_token

# Function to obtain the organization id based on the org name
def get_organization_id(access_token, org_name):
    complete_url = anypoint_platform_base_url + "/accounts/api/me"
    logging.info("Get organization id - Request: {}".format(complete_url))
    response = requests.get(url = complete_url, headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token})
    logging.info("Get organization id - Received status code: {}".format(response.status_code))
    org_id = None
    if response.status_code == 200:
        orgs_list = response.json()['user']['contributorOfOrganizations']
        for org in orgs_list:
            if org['name'].lower() == org_name.lower():
                org_id = org['id']
                logging.info("Get organization id - Response: {}".format(org_id))
                break
    else:
        logging.info("Get organization id - Response: failed: {}".format(str(response.status_code)))

    if not org_id :
        logging.info("Get organization id - Response: Organization name not found")
    
    print(org_id)
    return org_id

# Function to obtain the environment id based on the environment name
def get_environment_id(access_token, org_id, env_name):
    complete_url = anypoint_platform_base_url + "/accounts/api/organizations/" + org_id + "/environments"
    logging.info("Get environments info - Request: {}".format(complete_url))
    response = requests.get(url = complete_url, headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token})
    logging.info("Get environments info - Received status code: {}".format(response.status_code))
    env_id = None
    if response.status_code == 200:
        environments_info = dict(response.json())['data']
        for env in environments_info:
            if (env['name'].lower() == env_name.lower()):
                env_id = env['id']
                logging.info("Get environments info - Response: Environment id: {} for name: {}".format(env_id, env_name))
                break
    else:
        logging.info("Get environments info - Response: failed: {}".format(str(response.status_code)))

    if not env_id:
        logging.info("Get environments info - Response: Environment name not found")
    
    print(env_id)
    return env_id

