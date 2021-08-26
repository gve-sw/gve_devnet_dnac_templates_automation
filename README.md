# gve_devnet_dnac_templates_automation



## Contacts
* Danielle Stacy



## Solution Components
* DNA Center
* Cisco WLC/Switch
* Python 3.9



## Installation/Configuration

Installation

```
# Create Virtual Environment (MacOS)
python3 -m venv VirtualEnvironment
source VirtualEnvironment/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Configuration

In the env.py file, define any variables set to XXXXX
```python

env = {
    "base_url": "XXXXX", #dna center url
    "username": "XXXXX", #dna center username
    "password": "XXXXX", #dna center password
    "version": "XXXXX"   #dna center version
}

project_name = "XXXXX" #name of the project you want to associate template with
device_name = "XXXXX" #name of device you want to deploy template to
```

In the config.txt file, define the template/configuration you want to deploy.
```
!
!
template/configuration goes here!
!
end
```

In the dnac.py file in the create_Template function, you may define the template variables for your template.
```python
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
```



## Usage
To run the code to create and deploy a template:
```
$ python main.py
```
The program will output status messages as it progresses to indicate if it's successful at each step.



# Screenshots

Output from running the code
![/IMAGES/program-output.png](/IMAGES/program-output.png)

Template configured by the code
![/IMAGES/template.png](/IMAGES/template.png)

Output from show run of device that template provisioned
![/IMAGES/vlan-config.png](/IMAGES/vlan-config.png)

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
