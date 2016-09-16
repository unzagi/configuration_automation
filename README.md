Automation of NADs Router Configs
---------------------------------

Requirements
------------

1. Python 3 for Windows
2. Install jinja2 for Python 3s
3. Excel Spreadsheet of NADs templates for template specific information

Assumptions
-----------

1.Basic working knowledge of Python


Process - Generating the Jinja2 template
----------------------------------------

1. Find the old NADS configuration file that is being converted and copy it to the clipboard.
2. Open up template.jinja2 into a text editor

This template pulls through information based on some variables and just give an idea of when it was generated by, who generated it, what template is was based on and any other information pulled from the template spreadsheet.

    # < ------------ Start of Information Only - Do not apply  ------------>

	# {{hardware_make}} Template]
	# Template Generated
	# From jinja2 file: {{jinja2_template_name}}
	# On: {{date_time}}
	# By: {{engineer_name}}

	# For Device: {{hardware_model}}
	# Template name: {{template_name}}
	# Template has superseded: {{previous_template_name}}

	# Template specific information
	# Telco: {{telco_name}}
	# Circuit Name: {{circuit_name}}
	# Bandwidth: {{bandwidth}}
	# Routing Protocol: {{routing}}
	# Connection Type: {{connection_type}}
	# Number of Customer LANs Supported: {{customer_lans}}
	# Number of Static Routes supported: {{customer_static_routes}}
	# Out of Scope Configuration: {{out_of_scope}}

	# < ------------ End of Information Only - Do not apply  ------------>

	# < ------------ configuration start ------------>

	# Paste your configuration here, then set the variables based on jinja_variables_template and any additional one add to sed file.

	# < ------------ configuration end ------------>

3. Paste in the NADS config

Paste the configuration over the top of:

	# Paste your configuration here, then set the variables based on jinja_variables_template and any additional one add to sed file."

2. Technically assess the NADS configuration file for any changes that need to be made.

For e.g. The SRX300 Devices no longer require a SFP card to be added.
So the WAN interface variables can be set to ether Ge-0/0/6 or Ge-0/0/07. 
Therefore for this specific part of the configuration, I can turn the Ge-0/0/0 part of my config to a jinja2 variable.
This is helpful if we suddenly decide we don't want to use Ge-0/0/7 in the template, it can easily be changed.

Example Jinja2 template Configuration:

	# < ------------ configuration start ------------>
	# WAN IP Interfaces
	set interfaces {{ iface_wan_name }} vlan-tagging
	set interfaces {{ iface_wan_name }} description "WAN"
	set interfaces {{ iface_wan_name }} mtu 1518
	set interfaces {{ iface_wan_name }} vlan-tagging
	set interfaces {{ iface_wan_name }} description "WAN"
	set interfaces {{ iface_wan_name }} unit [PRI_WAN_VLAN] vlan-id [PRI_WAN_VLAN] description "msr1.th1 via TalkTalk - [CIRCUIT_REF]"
	set interfaces {{ iface_wan_name }} unit [PRI_WAN_VLAN] vlan-id [PRI_WAN_VLAN] family inet address [PRI_WAN_IP]/31
	set interfaces {{ iface_wan_name }} unit [SEC_WAN_VLAN] vlan-id [SEC_WAN_VLAN] description "msr2.tc1 via TalkTalk - [CIRCUIT_REF]"
	set interfaces {{ iface_wan_name }} unit [SEC_WAN_VLAN] vlan-id [SEC_WAN_VLAN] family inet address [SEC_WAN_IP]/31
	# < ------------ configuration end ------------>

3. Save this config as a .jinja2 file - with the naming convention of ##.jinja2 - where ## represents the NADS project template i.e. JU01.jinja2

Generate the Python Variable file
---------------------------------

1. In the next step of this process you will need to create a variable python config file.
I've already created a python template file in the template folder which looks like:
```python
# Import python time module
import time

# Variables Template
# Set the template specific description variables
hardwareMake = 'Juniper'
hardwareModel = 'Juniper SRX300'
projectTemplateName = 'template'
previousTemplateName = 'none'

#Router Template information
telcoName = 'Telco Name'
circuitName = 'Circuit Name'
bandwidth = 'bandwidth'
routing = 'routng protocol'
connectionType = 'Connection Type'
customerLans = 1
customerStaticRoutes = 0
outOfScope = "out of scope items"

#Generated File information
outputFileName = "template.txt"
jinja2TemplateName = 'template.jinja2'
dateNow = time.strftime("%c") # set the time/date
engineerName = 'Simon Brooks'

#Set the configuration file variables - use 'lowercase' and '_' for Jijna2 Variables
#These will be subject to change/additions based on the template
ifaceLanName = 'ge-0/0/0'
ifaceWanName = 'ge-0/0/7'
```

Informational Variables
-----------------------

There are informaional variables to be set:
1. the template specific variables set the type of hardware and also the old NADs template name and new NADS template name
2. The router template information all comes from the excel spreadsheet containing all the existing NADS templates
3. The generated file information needs to be set to the 
 1. What name you give the output text file e.g. template.txt or JU03-template.txt where JU03 = NADS template number
 2. What name you give the jinja2 file e.g. template.jinja2 or JU03.jinja2 where JU03 = NADS template number
 3. Leave 'dateNow' variable as this generates the current time/date
 4. The engineer name who has created the template

Configuration Variables
-----------------------

Note: At the moment I've only set 'ifaceLanName' and 'ifaceWanName'. 
This is mainly due to the fact I'm using automation to generate NADS templates and not to generate customer configurations. 
In an ideal world, NADS would be removed and python would generate the templates - but this is outside the scope and subject to debate.

The configuration variables need to match what has been defined in the jinja2 file.

For example, if you wanted to automate the hostname you could change the static jinja2 template by doing the following:

jinja2 template 


	# Hostname
	set system host-name [HOSTNAME]

	Change the configuration to:

	# Hostname
	set system host-name {{ hostname }}

Jinja2 templates requre two sets of curly brackets, and a varable name. For nice tidy variables I am using all lowercase with underscores if there are multiple words.

For my configuration variables, I would then need to define the values for hostname

	hostname = 'csr01.id00000.cpe.ifl.net'

The Main Router Template Python File
------------------------------------

6. The template generation python file

I've created a template file to create the configurations. This can almost certainly be improved, but since this is only being used to generate NADS configs we're sticking to a jinja2, python variables file and a router template
generation file to generate the configs.

This is the configuration file, written in python and commented.

```python
# Jinja2 Template from https://vimeo.com/120005103
# Requires Jinja2 to be installed into python- http://jinja.pocoo.org/docs/dev/intro/
# Requires a Jinja2 template file to have already been created and variables set

# import librarys
import jinja2
import os

# Variables
from jinja_variables_template import *

# Setup jinja2
# tell jinja2 where to load templates from ( this should be your current working directory)
loader = jinja2.FileSystemLoader(os.getcwd())

#Create a jinja2 environment and reference the above loader
jenv = jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

#Render the template based on jinja2 file name variable
template = jenv.get_template('template.jinja2')

#Render the configuration based on the variables then print the output
output = template.render(hardware_make=hardwareMake,hardware_model=hardwareModel,template_name=projectTemplateName,previous_template_name=previousTemplateName,jinja2_template_name=jinja2TemplateName, 
                         telco_name=telcoName,circuit_name=circuitName,bandwidth=bandwidth,routing=routing,connection_type=connectionType,customer_lans=customerLans,customer_static_routes=customerStaticRoutes,out_of_scope=outOfScope,
                         date_time=dateNow,engineer_name=engineerName,iface_lan_name=ifaceLanName,iface_wan_name=ifaceWanName)
#Write the configuration to file if the file does not already exist
if not os.path.exists(outputFileName):
    with open(outputFileName, 'wt') as f:
        f.write(output)
        print(output)
        print("\nTempate written to file: ",outputFileName)
else:
    print('n\Error: ',outputFileName,'already exists! Check and retry')
```

The python file is written in Python 3. To run this script the jinja2 module must be installed.

The bits that need to change when running this file on a new configuration file are:

 1. "from jinja_variables_template import * - this must be changed to your variables file e.g. jinja_ju03_variables. This line imports the variables directly into the main python file. 

 2. You MUST set the template name in the python configuration file to the jinja file you have created previously. Remember it looks for the file within the directory you are working in, so you need to make sure your jinja2 template 
exists in the same directory as the running python script. This is the same for the varables python file.
```python
#Render the template based on jinja2 file name variable
template = jenv.get_template('template.jinja2')
```
 3. output = tempate.render(longassline...) - so in here you list all of the i.jinja2 variables listed in the jinja2 template file, followed by the python variables we've listed in the python file. Remember, if you have 
created new variables you need to add them into here so they are automatically generated. The formatting rule I've set by here is - jinja2 variables are lowercase with underscores, and python variables are camel case.

 4. The last bit of code at the end doesnt need to change, but this basically states that if the text file already exists, dont output the file to text. 
I've chosen to do this so it doesn't keep ovewriting the files.
```python
#Write the configuration to file if the file does not already exist
if not os.path.exists(outputFileName):
    with open(outputFileName, 'wt') as f:
        f.write(output)
        print(output)
        print("\nTempate written to file: ",outputFileName)
else:
    print('n\Error: ',outputFileName,'already exists! Check and retry')
```
That's it. You should have everything you need to generate configuration files.
