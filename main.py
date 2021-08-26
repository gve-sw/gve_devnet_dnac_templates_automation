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
from dnac import *
from env import *
import time
import pprint

######################################
# SCRIPT
######################################

#get Auth token and save in environment variable
env['token'] = getAuthToken(env)

#get template to deploy from file
with open("config.txt", "r") as template_file:
    template_lines = template_file.readlines()
    template = ''.join(template_lines)

if 'token' in env:
    projects = get_Projects(env)
    for project in projects:
        if project['name'] == project_name: #looking for project that is specified in env.py
            project_id = project['id'] #project id is needed to create the template

    response = create_Template(env, project_id, template)
    template_response = response.json()["response"]
    pprint.pprint(template_response)

    task_id = template_response["taskId"] #task id is needed to get task information
    task = get_Task(env, task_id)
    pprint.pprint(task)
    while "data" not in task["response"].keys():
        print()
        print()
        pprint.pprint(task)
        time.sleep(1)
        task = get_Task(env, task_id)
    template_id = task["response"]["data"] #template id is stored in task info

    version_Template(env, template_id) #we need to version template in order to deploy it

    devices = get_Dnac_Devices(env)
    for device in devices:
        if device["hostname"] == device_name: #looking for device name that is specified in env.py
            device_id = device["id"]
    print()
    print()

    deployment = deploy_Template(env, device_name, device_id, template_id) #push template created to device specified in env.py
else:
    print("The auth token was not able to be retrieved")
