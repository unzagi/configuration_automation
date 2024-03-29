import os
import time
import sys
from shutil import copyfile

## Create the Router Template Folder

print("\nPlease enter the new router template folder name to be generated: ")
templateName = input()

print("The template name is: ",templateName)
print("Press Y if this is this correct?")
myChoice = input()

##if myChoice != "Y" :
##    print("Wrong Input") #Validation should go here
##
##else:
##    print("OK")

osPath = "working_templates"
osNewPath = osPath + "/" + templateName
print("\n*** Provisioning Required Files ***")

if not os.path.isdir(osNewPath):
    os.makedirs(osNewPath)
    print("Created folder in " + osNewPath)
else:
    print("Error: " + osNewPath + " already exists")
    print("Continuing.....")
    
## Copy the jinja2 template file and rename
osFolderSrc = "template_files"
osFileSrc = "template.jinja2"
osPathSrc = osFolderSrc + "/" + osFileSrc

osNewFileDst = templateName + ".jinja2"
osPathDst = osNewPath + "/" + osNewFileDst

if os.path.exists(osNewPath):
    print("\nCopying " + osPathSrc + " template file to: " + osPathDst)
    copyfile(osPathSrc, osPathDst)
    print("\nRenaming " + osPathSrc +" to file: " + osPathDst)
    print("\n*** File Copy Complete ***")
    time.sleep(5)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("\n*** NADs Config Loader ***")
    print("Destination : " + osPathDst)
    print("\nPlease enter the NADS template name: ")
    existingTemplate = input()

    print("\nPress enter then CTRL+Z on new line after pasting")
    print("\nPlease Paste in the NADs Configuration File below: ")
    inputConfiguration = sys.stdin.read()

    templatePathSrc = osNewPath + "/" + existingTemplate + ".txt"
    print(osNewPath)
    print(templatePathSrc)

    if not os.path.exists(templatePathSrc):
        with open(templatePathSrc, 'wt') as f:
            f.write(inputConfiguration)
            print("\nNADs template written to file: ",templatePathSrc)
    else:
        print('n\Error: ',templatePathSrc,'already exists!')

    f = open(osPathDst, "r")
    contents = f.readlines()
    f.close()

    contents.insert(27, inputConfiguration) # write to line 27 and apply input configuration

    #write the file
    f = open(osPathDst, "w") 
    contents = "".join(contents)
    f.write(contents)
    f.close()
    print("Written to file: ",osPathDst)

else:
    print('\nError: ',osPathSrc,'does not exist! Check and retry')
    
## Copy the python variables template file and rename
print(osFolderSrc)
osFileSrc = "jinja_variables_template.py"
osPathSrc = osFolderSrc + "/" + osFileSrc
print("osPathSrc: " + osPathSrc)
print(templateName)
osNewFileDst = "jinja2_" + templateName + "_variables.py"
print("osNewFileDst: " + osNewFileDst)
osPathDst = osNewPath + "/" + osNewFileDst
print("osPathDst: " + osPathDst)
print("osNewPath: "+ osNewPath)
if os.path.exists(osNewPath):

    copyfile(osPathSrc, osPathDst)

    
    print("osPathSrc: " + osPathSrc)
    print("\nCopying " + osPathSrc + " template file to: " + osPathDst)

## Copy the python template file and rename
print(osFolderSrc)
osFileSrc = "jinja-template.py"
osPathSrc = osFolderSrc + "/" + osFileSrc
print("osPathSrc: " + osPathSrc)
print(templateName)
osNewFileDst = "jinja2_" + templateName + "_main.py"
print("osNewFileDst: " + osNewFileDst)
osPathDst = osNewPath + "/" + osNewFileDst
print("osPathDst: " + osPathDst)
print("osNewPath: "+ osNewPath)
if os.path.exists(osNewPath):

    copyfile(osPathSrc, osPathDst)
    print("osPathSrc: " + osPathSrc)
    print("\nCopying " + osPathSrc + " template file to: " + osPathDst)



