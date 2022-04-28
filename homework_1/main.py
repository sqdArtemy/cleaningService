from CSV_converter import CsvToJson
from JSON_converter import JsonToCsv

# Asks which file we need
f_name = input("Input file name with an extension: ")
extention = f_name[f_name.find('.')+1:]

if(extention == "csv"):
    obj1 = CsvToJson() #  From CSV to JSON
    file = obj1.reader(file=f_name); #  opening file
    result = obj1.converter(input=file); # converting file
    obj1.writer(result,"output_1.json") # writing result
elif(extention == "json"):
    obj2 = JsonToCsv() #  From JSON to CSV
    file = obj2.reader(file = f_name) # opening file
    result = obj2.converter(input = file) # convert data
    obj2.writer(result, "output_2.csv")
else:
    print("Doesn`t support this extension !")
