import os
import time
import sys

print("\nPleae enter the router template name to be generated : ")
templateName = input()
print("The template name is: ",templateName)
print("Press Y if this is this correct?")
myChoice = input()

if myChoice != "Y" :
    print("Quitting")

else:
    print("OK")

osPath = JN0

if not os.path.isdir(osPath):
    os.path.isdir(osPath)
    #print(os.makedirs(osPath))

else:
    print("NO")
