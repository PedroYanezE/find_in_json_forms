import argparse
import json
import os


def traverse_directory(folder_path, paths=[]):
    obj = os.scandir(folder_path)

    if verbose:
        print("-" * (2 + len(folder_path)))
        print(" " + folder_path + " ")
        print("-" * (2 + len(folder_path)) + "\n")

    for entry in obj:
        if entry.is_dir() and entry.name != ".git":
            if verbose:
                print()
            paths = traverse_directory(folder_path + "\\" + entry.name, paths)
        elif entry.is_file() and entry.name != ".gitignore":
            if verbose:
                print(entry.name)
            paths.append(entry.path)

    return paths


def check_parameters(field, is_array=False):
    """Checks if the form field has the searched parameters in it and if they match the specified value."""

    for match in matchs:
        parameter, value = match.split("=")

        if parameter not in field or field[parameter] != value:
            return False

    for parameter in has_parameters:
        if parameter not in field:
            return False

    return True


def search_in_form(form_object, found, is_array=False):
    for field in form_object:
        if field["type"] == "ARRAY":
            form_from_group = field["groupPrototype"]
            search_in_form(form_from_group, found, is_array=True)
        elif field["type"] == "GROUP":
            form_from_group = field["group"]
            search_in_form(form_from_group, found)
        else:
            if check_parameters(field, is_array):
                found.append(field)


def search_in_forms(json_form_paths, found=[]):
    """Calls search_in_form for every json form in the list of paths."""

    for json_form_path in json_form_paths:
        with open(json_form_path, encoding="utf-8") as json_form:
            form_object = json.load(json_form)
            search_in_form(form_object, found)

    return found


def main():
    folder_path = r"C:\Users\pedro\source\repos\bha-fichamedicaapi\dynFormsDefinitions\BradFord Hill"
    json_paths = traverse_directory(folder_path)
    found = search_in_forms(json_paths)

    print("Found ", len(found), " fields with the specified parameters and values.")

    for i in found:
        print(i)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        default=False,
        dest="verbose",
        help="Output extra information as it runs",
    )
    parser.add_argument(
        "-m",
        "--matchs",
        default=[],
        dest="matchs",
        help="Search for json form with a parameter that matches specified value. Ex: -m type=TEXT,url=localhost:4000",
    )
    parser.add_argument(
        "-hp",
        "--has_parameters",
        default=[],
        dest="has_parameters",
        help="Search for json form that has a parameter, not necessarily with a specified value. Ex: -hp type,url"
    )

    args = parser.parse_args()

    if not (args.matchs or args.has_parameters):
        parser.error("Either -m or -hp must be specified. Exiting.")

    verbose = args.verbose

    if args.matchs:
        matchs = args.matchs.split(",")
    else:
        matchs = []

    if args.has_parameters:
        has_parameters = args.has_parameters.split(",")
    else:
        has_parameters = []

    main()
