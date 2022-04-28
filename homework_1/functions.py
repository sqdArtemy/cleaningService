import abc # imports
import os.path
# created this file to avoid circular imports

# abstract classes
class AbstractConverter(abc.ABC): #  abstract class for converter
    @abc.abstractmethod
    def reader(self, file):
        pass
    def converter(self, input):
        pass
    def writer(self, output):
        pass

# functions
def empty_checker(file): #  checks if file is empty
    size = os.path.getsize(file);
    if size == 0: raise Exception("File is empty !")

def existance_checker(file): #  checks if file is already exists
    if os.path.exists(file):
        raise Exception("File is already exists !")

def file_writer(data, file): #  function that writes content to a particular file
    existance_checker(file)
    try:
        with open(file, "w") as f:  # writing converted data to a file
            f.write(data)
    except FileNotFoundError: #  checking if file is exists, otherwise troubleshoot an exception
        print("Seems like file is not here :(")

def file_opener(file): #  opens file
    try:
        f = open(file)
        empty_checker(file)
        return f
    except FileNotFoundError:
        print("File is not here !")
