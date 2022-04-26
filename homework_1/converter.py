import abc, json #  import needed libraries
from  json import JSONDecodeError


class AbstractConverter(abc.ABC): #  abstract class for converter
    @abc.abstractmethod
    def converter(self, input, output):
            pass


def file_writer(data, file): #  function that writes content to a particular file
    try:
        with open(file, "w") as f:  # writing converted data to a file
            f.write(data)
    except FileNotFoundError: #  checking if file is exists, otherwise troubleshoot an exception
        print("Seems like file is not here :(")


class CsvToJson(AbstractConverter): #  converter from CSV to JSON
    def converter(self, input, output):
            counter = 0; content = {}; converted = []
            with open(input, "r") as csv_file:
                for line in csv_file:
                    data = tuple(line.split(',')) #  Getting a tuple of values instead of single line

                    if counter == 0: #  converts first row to dictionary keys
                        for key in data: content[key.replace("\n", "")] = ""
                    else:
                        i = 0
                        for key in content: content[key] = data[i].replace("\n", ""); i+=1
                        converted.append(dict(content)) #  append values of dictionary, not a pointer of it
                    counter += 1
                if len(converted) <= 1: converted = converted[0];

            file_writer(data = json.dumps({"data:": converted}), file = output) #  calling a function that writes to a file


class JsonToCsv(AbstractConverter): #  Converter from JSON to CSV
    def converter(self, input, output):
        with open(input, "r") as json_file:
            data = {}
            result = str()

            try:
                data = json.load(json_file)
            except JSONDecodeError:  # Handling some error cases
                print("I suppose, that file is empty :(")

            for i in data:
                dictionaries = data[i]
                records = [dictionaries[0].keys(),] # Adds first row as a reference values(name tags)
                for dict in dictionaries: records.append(dict.values())
                for j in records: result += (",".join(j) + "\n")
            file_writer(data = result, file = output) #  calling funtion that writes to a file

obj1 = CsvToJson(); obj1.converter("input_1.csv", "output_1.json")
obj2 = JsonToCsv(); obj2.converter("input_2.json", "output_2.csv")