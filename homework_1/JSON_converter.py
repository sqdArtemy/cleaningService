from functions import *
class JsonToCsv(AbstractConverter): #  Converter from JSON to CSV
    def reader(self, file): #  reads file
        return file_opener(file)

    def converter(self, input): #  method to convert input
        result = str();
        data = {}
        try:
            data = eval(input.read().replace("\n", ""))  # reading json file to dict
        except SyntaxError:
            print("Looks like file is empty !")

        for i in data:
            dictionaries = data[i]
            records = [d.values() for d in dictionaries]  # Using list comprehension in order to convert data
            records.insert(0, dictionaries[0])
            for j in records: result += (",".join(j) + "\n")
        return result  # return converted output

    def writer(self, data, output): #  method to write to a file
        file_writer(data = data, file = output) #  calling function that writes converted to a file
