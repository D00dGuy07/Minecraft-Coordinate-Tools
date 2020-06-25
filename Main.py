# Minecraft Coordinate Tools
# By Kieran Brown

import importlib
from Library import library

import os
clear = lambda: os.system('cls')
clear()

frameworkFiles = [
    "Main.py",
    "Library.py",
    "Errors.py"
]

print("Minecraft Coordinate Tools\nVersion: 1.0\n")

files = os.listdir()
modules = []

for _file in files:
    if ".py" in _file and not _file in frameworkFiles:
        modules.append(_file[:-3])

print("Choose a tool to use from this list:")

toolIndex = 0

for index, module in enumerate(modules):
    modules[index] = importlib.import_module(module)
    moduleName = modules[index].getInfo()
    print("{0}) {1}".format(index + 1, moduleName))
print("")

while True:
    toolIndex = input()
    if toolIndex.isdigit() and toolIndex != "0" and int(toolIndex) <= len(modules):    
        break
    else:
        print("You have to choose a number in the range of the choices")

clear()

modules[int(toolIndex) - 1].start(library())