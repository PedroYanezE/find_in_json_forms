import argparse
import json
import os

def traverse_directory(folder_path, paths = []):
    obj = os.scandir(folder_path)

    if(verbose):
        print("-"*(2+len(folder_path)))
        print(" " + folder_path + " ")
        print("-"*(2+len(folder_path))+ "\n")

    for entry in obj:
        if entry.is_dir() and entry.name != ".git":
            if(verbose):
                print()
            paths = traverse_directory(folder_path + "\\" + entry.name, paths)
        elif entry.is_file() and entry.name != ".gitignore":
            if(verbose):
                print(entry.name)
            paths.append(entry.path)

    return(paths)

def check_parameters_in_field(field):
    """Checks if the form field has the searched parameters in it, and if the excluded parameters aren't."""

    for parameter in parameters:
        if parameter[0] == "!":
            if parameter[1:] in field:
                return(False)
        else:
            if(parameter not in field or field[parameter] == ""):
                return(False)

    return(True)

def search_in_form(form_object, found, myFlag):
    for field in form_object:
        if(field['type'] == "ARRAY"):
            form_from_group = field['groupPrototype']
            search_in_form(form_from_group, found, myFlag = True)
        elif(field['type'] == "GROUP"):
            form_from_group = field['group']
            search_in_form(form_from_group, found, myFlag = True)
        else:
            if(check_parameters_in_field(field)):
                found.append(field)

def search_in_forms(json_form_paths, found = []):
    """Calls search_in_form for every json form in the list of paths."""

    if parameters == []:
        return([])

    for json_form_path in json_form_paths:
        with open(json_form_path, 'r') as json_form:
            form_object = json.load(json_form)
            search_in_form(form_object, found, False)

    return(found)

def main():
    folder_path = r'C:\Users\pedro\source\repos\bha-fichamedicaapi\dynFormsDefinitions\BradFord Hill'
    json_paths = traverse_directory(folder_path)
    found = search_in_forms(json_paths)

    print("Found " + str(len(found)) + " fields with the parameters: " + str(parameters) + "\n")

    for i in found:
        print(i)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", default=False, dest='verbose',help="output extra information as it runs")
    parser.add_argument("-p", "--parameters", default=[], dest='parameters',help="parameters to search in the fields of the json forms")
    verbose = parser.parse_args().verbose
    parameters = parser.parse_args().parameters.split(',')

    main()
