import os
import Errors
import math

class library:
    def __init__(self):
        self.DataBase = DataBase()

    def Clear(self):
        clear = lambda: os.system('cls')
        clear()

    def Vector3(self, X, Y, Z):
        return Vector3(X, Y, Z)

    def Vector2(self, X, Y):
        return Vector2(X, Y)

    def RepresentsInt(self, value):
        return RepresentsInt(value)

    def RepresentsFloat(self, value):
        return RepresentsFloat(value)

class DataBase:
    def __init__(self):
        scriptDirectory = os.path.dirname(__file__)
        relativePath = "Lists"
        self.ListDirectory = os.path.join(scriptDirectory, relativePath)
    
    def CheckDictionaryFile(self, name):
        fileToCheck = os.path.join(self.ListDirectory, name + ".dict")
        return os.path.isfile(fileToCheck)

    def GetDictionaryFiles(self):
        files = os.listdir(self.ListDirectory)
        for _file in files:
            if not(_file.endswith(".dict")):
                files.remove(_file)
        return files

    def SaveDictionary(self, name, dictionary):
        fileToOpen = os.path.join(self.ListDirectory, name + ".dict")

        with open(fileToOpen, "w") as saveFile:
            for key, content in dictionary.items():
                if isinstance(content, str):
                    content = '"{0}"'.format(content)

                saveFile.write("{0} : {1}\n".format(key, content))
    
    def LoadDictionary(self, name):
        fileToOpen = os.path.join(self.ListDirectory, name + ".dict")

        loadingDict = {}
        with open(fileToOpen, "r") as loadFile:    
            for line in loadFile:
                separation = line.find(":")
                key = line[:separation - 1]
                content = line[separation + 2:]

                if content.startswith("("):
                    content = ParseVector(content)
                
                loadingDict[key] = content
            return loadingDict

class Vector3:
    def __init__(self, X, Y, Z):
        if RepresentsFloat(X) and RepresentsFloat(Y) and RepresentsFloat(Z):
            self.X = X
            self.Y = Y
            self.Z = Z
        else:
            raise Errors.Vector3ValueError("Vector3 requires float or integer values to initialize succesfully")

    def ConvertToVector2(self):
        return Vector2(self.X, self.Z)
    
    def __str__(self):
        return "({0}, {1}, {2})".format(self.X, self.Y, self.Z)
    
    def __add__(self, other):
        if isinstance(other, Vector3):
            result = Vector3(self.X + other.X, self.Y + other.Y, self.Z + other.Z)
        if isinstance(other, int) or isinstance(other, float):
            result = Vector3(self.X + other, self.Y + other, self.Z + other)
        return result
    
    def __sub__(self, other):
        if isinstance(other, Vector3):
            result = Vector3(self.X - other.X, self.Y - other.Y, self.Z - other.Z)
        if isinstance(other, int) or isinstance(other, float):
            result = Vector3(self.X - other, self.Y - other, self.Z - other)
        return result

    def __mul__(self, other):
        if isinstance(other, Vector3):
            result = Vector3(self.X * other.X, self.Y * other.Y, self.Z * other.Z)
        if isinstance(other, int) or isinstance(other, float):
            result = Vector3(self.X * other, self.Y * other, self.Z * other)
        return result

    def __truediv__(self, other):
        if isinstance(other, Vector3):
            result = Vector3(self.X / other.X, self.Y / other.Y, self.Z / other.Z)
        if isinstance(other, int) or isinstance(other, float):
            result = Vector3(self.X / other, self.Y / other, self.Z / other)
        return result
    
    def __floordiv__(self, other):
        if isinstance(other, Vector3):
            result = Vector3(self.X // other.X, self.Y // other.Y, self.Z // other.Z)
        if isinstance(other, int) or isinstance(other, float):
            result = Vector3(self.X // other, self.Y // other, self.Z // other)
        return result

    def __floor__(self):
        result = Vector3(math.floor(self.X), math.floor(self.Y), math.floor(self.Z))
        return result

    def __ceil__(self):
        result = Vector3(math.ceil(self.X), math.ceil(self.Y), math.ceil(self.Z))
        return result

class Vector2:
    def __init__(self, X, Y):
        if RepresentsFloat(X) and RepresentsFloat(Y):
            self.X = X
            self.Y = Y
        else:
            raise Errors.Vector2ValueError("Vector2 requires float or integer values to initialize succesfully")
    
    def __str__(self):
        return "({0}, {1})".format(self.X, self.Y)
    
    def __add__(self, other):
        if isinstance(other, Vector2):
            result = Vector2(self.X + other.X, self.Y + other.Y)
        if isinstance(other, int) or isinstance(other, float):
            result = Vector2(self.X + other, self.Y + other)
        return result
    
    def __sub__(self, other):
        if isinstance(other, Vector2):
            result = Vector2(self.X - other.X, self.Y - other.Y)
        if isinstance(other, int) or isinstance(other, float):
            result = Vector2(self.X - other, self.Y - other)
        return result

    def __mul__(self, other):
        if isinstance(other, Vector2):
            result = Vector2(self.X * other.X, self.Y * other.Y)
        if isinstance(other, int) or isinstance(other, float):
            result = Vector2(self.X * other, self.Y * other)
        return result

    def __truediv__(self, other):
        if isinstance(other, Vector2):
            result = Vector2(self.X / other.X, self.Y / other.Y)
        if isinstance(other, int) or isinstance(other, float):
            result = Vector2(self.X / other, self.Y / other)
        return result
    
    def __floordiv__(self, other):
        if isinstance(other, Vector2):
            result = Vector2(self.X // other.X, self.Y // other.Y)
        if isinstance(other, int) or isinstance(other, float):
            result = Vector2(self.X // other, self.Y // other)
        return result
    
    def __floor__(self):
        result = Vector2(math.floor(self.X), math.floor(self.Y))
        return result

    def __ceil__(self):
        result = Vector2(math.ceil(self.X), math.ceil(self.Y))
        return result

def ParseVector(content):
    if content.startswith("("):
        content = content[1:-1]
        
        vectorValues = []
        while True:
            comma = content.find(",")
            if comma == -1:
                vectorValues.append(content[:-1])
                break

            vectorValues.append(content[:comma])
            content = content[comma + 2:]
        if len(vectorValues) == 2:
            return Vector2(int(vectorValues[0]), int(vectorValues[1]))
        elif len(vectorValues) == 3:
            return Vector3(int(vectorValues[0]), int(vectorValues[1]), int(vectorValues[2]))
        else:
            raise Errors.ParsingError("Vector value had wrong amount of values")
    else:
        raise Errors.ParsingError("ParseVector function did not get a vector to parse")

def RepresentsFloat(value):
    try: 
        float(value)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def RepresentsInt(value):
    try: 
        int(value)
        return True
    except ValueError:
        return False
    except TypeError:
        return False