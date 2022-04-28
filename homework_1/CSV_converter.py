from functions import *

class CsvToJson(AbstractConverter): #  converter from CSV to JSON
    def reader(self, file):
        return file_opener(file)

    def converter(self, input):
        counter = 0; content = {}; converted = []
        for line in input:
            data = tuple(line.split(','))  # Getting a tuple of values instead of single line

            if counter == 0:  # converts first row to dictionary keys
                for key in data: content[key.replace("\n", "")] = ""
            else:
                i = 0
                for key in content: content[key.replace("\n", "")] = data[i].replace("\n", ""); i += 1
                converted.append(dict(content))  # append values of dictionary, not a pointer of it
            counter += 1
        if len(converted) <= 1: converted = converted[0];
        input.close()  # closing file
        return str({"data:": converted}).replace("'", '"')

    def writer(self,data, output):
        file_writer(data=data, file=output)  # calling a function that writes to a file