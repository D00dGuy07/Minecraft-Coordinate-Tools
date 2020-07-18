# List Location creates a list of locations tied to names
# By Kieran Brown

name = "Locations List"
description = "Creates a set of coordinates with names"


def getInfo():
    return "{0} - {1}".format(name, description)

commands = {
    "add" : "[Name] [X] [Y] [Z] | Adds location to the list",
    "list" : "| Shows list",
    "remove" : "[Name] | Removes entry",
    "rename" : "[Old Name] [New Name] | Renames entry",
    "edit" : "[Name] [New X] [New Y] [New Z] | Edits entry",
    "exit" : "| Closes application",
    "save" : "[Name] | Saves list",
    "open" : "| Opens prompt to open a list"
}

def start(library):  
    print('Locations List Tool\n\nJust type "exit" to go back to the main menu.\nFor names if you want spaces then surround it with "(curly brackets)"\n')
    
    print("List of commands:")

    defaultSpace = 35
    for command, information in commands.items():
        barPosition = information.find("|")
        spaces = defaultSpace - barPosition - len(command)
        parameters = " " + information[:barPosition]
        description = information[barPosition:]
        

        print("{0}{1}{3}{2}".format(command, parameters, description, " " * spaces))

    print("")

    locationsList = {}
    saved = True

    defaultReturn = {
        "exit" : False,
        "saved" : True,
        "locationsList" : None
    }

    while True:
        arguments = seperateArguments(input())

        if len(arguments) < 0:
            print("You have to use a command.")

        elif arguments[0] in commandAssignedFunctions.keys():
            result = commandAssignedFunctions[arguments[0]](arguments, library, locationsList, defaultReturn)

            if result:
                saved = result["saved"]
                defaultReturn["saved"] = saved

                if result["locationsList"]:
                    locationsList = result["locationsList"]

                if result["exit"] == True:
                    break

            

def seperateArguments(command):
    arguments = []

    while True:
        if command == "":
            break
        
        if command.startswith("("):
            endBracket = command.find(")")
            arguments.append(command[1:endBracket])
            command = command[endBracket + 2:]
        else:
            firstSpace = command.find(" ")
            if firstSpace == -1:
                arguments.append(command)
                break
            
            arguments.append(command[:firstSpace])
            command = command[firstSpace + 1:]
    
    return arguments


#Command Functions

def add(arguments, library, locationsList, defaultReturn):
    results = defaultReturn

    if len(arguments) != 5:
        print("You did not inclue the exact amount of info required for the add command.")
        return
    elif arguments[1] in locationsList.keys():
        print("There is already an entry in this list under this name. Would you like to overwrite it? (y/n)")
        decision = input()

        if decision == "y":
            results = edit(arguments, library, locationsList, defaultReturn)
            return results
        else:
            return
    elif not(library.RepresentsInt(arguments[2]) and library.RepresentsInt(arguments[3]) and library.RepresentsInt(arguments[4])):
        print("You must put numbers as the coordinates.")
        return
    else:
        newLocation = library.Vector3(int(arguments[2]), int(arguments[3]), int(arguments[4]))
        locationsList[arguments[1]] = newLocation
        
        results["saved"] = False
        results["locationsList"] = locationsList
        return results
  

def _list(arguments, library, locationsList, defaultReturn):
    if len(arguments) > 1:
        print("The list command does not require parameters.")
        return

    counter = 0
    for name, location in locationsList.items():
        counter += 1
        print("{0}) {1} | {2}".format(counter, name, str(location)))
    

def remove(arguments, library, locationsList, defaultReturn):
    results = defaultReturn
    
    if len(arguments) != 2:
        print("You did not inclue the exact amount of info required for the remove command.")
        return
    elif not(arguments[1] in locationsList.keys()):
        print("There is no entry in this list under the name {0}".format(arguments[1]))
        return
    else:
        locationsList.pop(arguments[1])

        results["locationsList"] = locationsList
        results["saved"] = False
        return results


def rename(arguments, library, locationsList, defaultReturn):
    results = defaultReturn

    if len(arguments) != 3:
        print("You did not inclue the exact amount of info required for the rename command.")
        return
    elif not(arguments[1] in locationsList.keys()):
        print("There is no entry in this list under the name {0}".format(arguments[1]))
    else:
        locationsList[arguments[2]] = locationsList.pop(arguments[1])

        results["locationsList"] = locationsList
        results["saved"] = False
        return results


def edit(arguments, library, locationsList, defaultReturn):
    results = defaultReturn

    if len(arguments) != 5:
        print("You did not inclue the exact amount of info required for the edit command.")
        return
    elif not(arguments[1] in locationsList.keys()):
        print("There is no entry under that name. Would you like to make one?(y/n)")

        decision = input()
        if decision == "y":
            results = add(arguments, library, locationsList, defaultReturn)
            return results
        else:
            return
    elif not(library.RepresentsInt(arguments[2]) and library.RepresentsInt(arguments[3]) and library.RepresentsInt(arguments[4])):
        print("You must put numbers as the coordinates.")
        return
    else:
        newLocation = library.Vector3(int(arguments[2]), int(arguments[3]), int(arguments[4]))
        locationsList[arguments[1]] = newLocation

        results["locationsList"] = locationsList
        results["saved"] = False
        return results


def _exit(arguments, library, locationsList, defaultReturn):
    results = defaultReturn

    if results["saved"]:
        results["exit"] = True
        return results
    else:
        print("You have not saved your list, are you sure you would like to exit?(y/n)")
        
        decision = input()
        if decision == "y":
            results["exit"] = True
            return results
        else:
            return


def save(arguments, library, locationsList, defaultReturn):
    results = defaultReturn

    if len(arguments) != 2:
        print("You did not include the exact amount of info required for the save command.")
        return
    elif len(locationsList) < 1:
        print("You need to add something to the list before it can be saved.")
        return
    elif library.DataBase.CheckDictionaryFile(arguments[1]):
        print("The file you would like to save to already exists:\n1) Overwrite the file\n2) See contents of file\n3) Cancel operation")
        
        while True:
            decision = input()

            if not(library.RepresentsInt(decision)):
                print("You have to put a number.")
            elif int(decision) < 1 or int(decision) > 3:
                print("You have to put a number in the range of 1 to 3.")
            elif int(decision) == 1:
                library.DataBase.SaveDictionary(arguments[1], locationsList)
                results["saved"] = True
                return results
            elif int(decision) == 2:
                contents = library.DataBase.LoadDictionary(arguments[1])
                _list([], library, contents, defaultReturn)

                print("You have the same options:\n1) Overwrite the file\n2) See contents of file\n3) Cancel operation")
            elif int(decision) == 3:
                return
    else:
        library.DataBase.SaveDictionary(arguments[1], locationsList)

        results["saved"] = True
        return results
 

def _open(arguments, library, locationsList, defaultReturn):
    results = defaultReturn

    if len(arguments) > 1:
        print("You don't need any parameters for the open command")
    else:
        files = library.DataBase.GetDictionaryFiles()
        
        print("Chose a file to open:")
        
        count = 0
        for _file in files:
            count += 1
            print("{0}) {1}".format(count, _file[:-5]))
        
        print("")

        fileToOpen = input()
        loadedFile = None
        
        while True:
            if library.RepresentsInt(fileToOpen):
                results["locationsList"] = library.DataBase.LoadDictionary(files[int(fileToOpen) - 1][:-5])
                results["saved"] = True
                return results
            else:
                print("Pick the number of the file.")
                fileToOpen = input()
    

commandAssignedFunctions = {
    "add" : add,
    "list" : _list,
    "remove" : remove,
    "rename" : rename,
    "edit" : edit,
    "exit" : _exit,
    "save" : save,
    "open" : _open
}