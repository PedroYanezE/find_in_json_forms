import argparse
import json
import os


def traverse_directory(folder_path, paths=[]):
    """Traverses the directory and returns a list of paths to json forms."""
    obj = os.scandir(folder_path)

    for entry in obj:
        if entry.is_dir() and entry.name != ".git":
            paths = traverse_directory(folder_path + "\\" + entry.name, paths)
        elif entry.is_file() and entry.name != ".gitignore":
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
    """Appends fields in the form that fulfill the required conditions."""
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
    json_paths = traverse_directory(r'{}'.format(main_path))
    found = search_in_forms(json_paths)

    print("Found ", len(found), " fields with the specified parameters and values.")

    for i in found:
        print(i)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path",
        default=[],
        dest="path",
        help="Path to the folder containing the json forms.",
        required=True
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

    main_path = args.path

    if args.matchs:
        matchs = args.matchs.split(",")
    else:
        matchs = []

    if args.has_parameters:
        has_parameters = args.has_parameters.split(",")
    else:
        has_parameters = []

    main()
