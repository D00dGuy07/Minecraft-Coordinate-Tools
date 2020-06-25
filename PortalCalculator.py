# Portal Calculator takes a file made in locations list and calculates those coordinates in the nether
# By Kieran Brown

import math

name = "Portal Calculator"
description = "Takes a save file made in Locations List and calculates those coordinates in the nether"


def getInfo():
    return "{0} - {1}".format(name, description)

def start(library):
    print("Portal Calculator\nYou have to make a list in the Locations List tool to use this.\nThis tool will convert these files to portal coordinates but in a copy.\n")

    files = library.DataBase.GetDictionaryFiles()

    print("Chose a file to convert:")

    count = 0
    for _file in files:
        count += 1
        print("{0}) {1}".format(count, _file[:-5]))
    print("")

    fileToOpen = input()

    loadedFile = None
    while True:
        if library.RepresentsInt(fileToOpen):
            locationsList = library.DataBase.LoadDictionary(files[int(fileToOpen) - 1][:-5])
            break
        else:
            print("Pick the number of the file.")
            fileToOpen = input()

    for name, coordinate in locationsList.items():
        locationsList[name] = convertToNetherCoords(coordinate.ConvertToVector2(), library)
    
    print("Choose a name for the file:")
    fileName = input()

    library.DataBase.SaveDictionary(fileName, locationsList)
    
def convertToNetherCoords(coordinate, library):
    return coordinate / 8