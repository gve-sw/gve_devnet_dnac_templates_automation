#!/usr/bin/env python3
"""
#Copyright (c) 2020 Cisco and/or its affiliates.
#
#This software is licensed to you under the terms of the Cisco Sample
#Code License, Version 1.1 (the "License"). You may obtain a copy of the
#License at
#
#               https://developer.cisco.com/docs/licenses
#
#All use of the material herein must be in accordance with the terms of
#the License. All rights not expressly granted by the License are
#reserved. Unless required by applicable law or agreed to separately in
#writing, software distributed under the License is distributed on an "AS
#IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#or implied.
"""
import requests
import time
import pprint
import urllib3

urllib3.disable_warnings()

def getAuthToken(env):
	"""
	Intent-based Authentication API call
	The token obtained using this API is required to be set as value to the X-Auth-Token HTTP Header
	for all API calls to Cisco DNA Center.
	:param env:
	:return: Token STRING
	"""
	url = '{}/dna/system/api/v1/auth/token'.format(env['base_url'])
	# Make the POST Request
	response = requests.post(url, auth=(env['username'], env['password']), verify=False)

	# Validate Response
	if 'error' in response.json():
		print('ERROR: Failed to retrieve Access Token!')
		print('REASON: {}'.format(response.json()['error']))

	else:
		return response.json()['Token'] #return only the token


def get_Dnac_Devices(env):
	url = '{}/dna/intent/api/v1/network-device'.format(env['base_url'])
	headers = {
		'x-auth-token': env['token'],
		'Content-Type': 'application/json',
		'Accept': 'application/json'
	}
	# Make the GET Request
	response = requests.get(url, headers=headers, verify=False)

	# Validate Response
	if 'error' in response.json():
		print('ERROR: Failed to retrieve Network Devices!')
		print('REASON: {}'.format(response.json()['error']))
		return []
	else:
		return response.json()['response'] #return the list of dnac devices


def create_Template(env, project_id, template):
    url = "{}/dna/intent/api/v1/template-programmer/project/{}/template".format(env["base_url"], project_id)
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
    }
    payload = {
        "description": "give the template a description",
        "deviceTypes": [
            {
                "productFamily": "Switches and Hubs"
                #choose a product family that matches the product you want to configure
                #product families you may pick include: Cisco UCS Series, Meraki Access Point, Meraki Security Appliances, Meraki Switches, NFVIS, Routers, Switches and Hubs, Autonomous AP, Wireless Controller, Unified AP, etc
            }
        ],
        "name": "Demo_Template", #name of template
        "softwareType": "IOS-XE",
        #choose a software type that matches the device you want to configure
        #Software types include: IOS, IOS-XE, IOS-XR, NX-OS, Cisco Controller, Wide Area Application Services, Adaptive Security Appliance, NFV-OS, and Others
        "templateContent": template #template content specified in config.txt
    }
    # Make the POST Request
    response = requests.post(url, headers=headers, json=payload, verify=False)

    # Need the response to check task progress
    return response


def deploy_Template(env, hostname, device_id, template_id):
    url = "{}/dna/intent/api/v1/template-programmer/template/deploy".format(env["base_url"])
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
    }
    payload = {
        "targetInfo": [
            {
                "hostName": hostname, #hostname specified in env.py
                "type": "MANAGED_DEVICE_UUID",
                "id": device_id
            }
        ],
        "templateId": template_id
    }

    # Make POST request
    response = requests.post(url, headers=headers, json=payload, verify=False)

    # Check deployment status
    if response.status_code == 200 or response.status_code == 202:
        pprint.pprint(response.json())

        if "not deploying" in response.json()["deploymentId"]:
            print("Device %s not applicable for deployment of template %s. Hence, not deploying"%(hostname, template_id))
        else:
            print("Successfully deployed template %s to %s"%(template_id, hostname))

            while True:
                if "IN_PROGRESS" == check_Deployment_Status(env,
                    response.json()["deploymentId"].partition("Template Deployemnt Id: ")[2]):
                    time.sleep(2)
                    continue
                else:
                    break

            return response.json()

    else:
        print("Did not deploy template %s to %s"%(template_id, hostname))


def get_Task(env, task_id):
    url = "{}/dna/intent/api/v1/task/{}".format(env["base_url"], task_id)
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
    }

    # Make GET request
    response = requests.get(url, headers=headers, verify=False)

    return response.json() #return response with information about specific task


# A template must be versioned before it can be deployed
def version_Template(env, template_id):
    url = "{}/dna/intent/api/v1/template-programmer/template/version".format(env["base_url"])
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
    }
    payload = {
        "templateId": template_id
    }

    # Make POST request
    response = requests.post(url, headers=headers, json=payload, verify=False)
    pprint.pprint(response.text)


# Need a way to check if deployment of template to device was successful
def check_Deployment_Status(env, deployment_id):
    url = "{}/dna/intent/api/v1/template-programmer/template/deploy/status/{}".format(env["base_url"], deployment_id)
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
    }

    # Make GET request
    response = requests.get(url, headers=headers, verify=False)
    pprint.pprint(response.json())

    return response.json()["devices"][0]["status"] #return the deployment status


# Need a way to pull a list of the projects and their ids
def get_Projects(env):
    url = "{}/dna/intent/api/v1/template-programmer/project".format(env["base_url"])
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, verify=False)

    return response.json()
