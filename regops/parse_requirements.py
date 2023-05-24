import glob
from typing import Union


# strip new lines of end of string
# replace || with space as this is our delimiter
def strip_chars(value: Union[str, None]) -> str:
    if value is not None and value != "":
        value = value.replace("\n", " ")
        value = value.replace("||", " ")
        if value[-1] == " ":
            value = value[:-1]
    return value


def parseRequirements() -> dict[str, list[str]]:
    # find all requirements.txt files
    requirement_files = glob.glob("../app/**/requirements.txt", recursive=True)
    # initialise variables
    temp_requirement_comments = {}
    requirement_comments = {}

    # iterating over all requirements.txt files
    for file in requirement_files:
        with open(file, "r") as source:
            # load file into memory
            lines = source.readlines()
            for line in lines:
                # if the line is not a comment
                if not line.startswith("#"):
                    # this is a package
                    package_name = line
                    if "==" in package_name:
                        # this is a versioned package, strip off version
                        package_name = line.split("==")[0]
                    package_name = strip_chars(package_name)
                    # initialise package in dictionary
                    temp_requirement_comments[package_name] = ["", ""]
                else:
                    # it must be a comment
                    # remove the # from the start of the line
                    line = line[2:]
                    if line.startswith("URL: "):
                        # this is a URL
                        temp_requirement_comments[package_name][0] = line[5:]
                    else:
                        # this is the comment's body
                        temp_requirement_comments[package_name][1] += line

    # iterating over the temporary dictionary,
    # stripping new lines and || from the end of each value
    # then adding it to the final dictionary
    for library_name, details in temp_requirement_comments.items():
        requirement_comments[strip_chars(library_name)] = [
            strip_chars(details[0]),
            strip_chars(details[1]),
        ]

    # returns dictionary containing package name, url and comment
    return requirement_comments
