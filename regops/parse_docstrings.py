import glob
import ast
import yaml
from typing import Union

# Constants
start_indicator = "-----BEGIN HAZARDS-----"
end_indicator = "-----END HAZARDS-----"
valid_likelihoods = ["Very high", "High", "Medium", "Low", "Very low"]
valid_severities = ["Minor", "Significant", "Considerable", "Major", "Catastrophic"]

# load config from yaml
config = yaml.safe_load(open("regops_config.yaml"))["regops"]

# set replacements (what in template will be replaced with what)
replacements = {
    "APPLICATION_NAME": config["application_name"],
    "OWNER": config["owner"],
    "AUTHORS": config["authors"],
}

# define risk matrix (likelihood, consequence)
# risk_matrix[index of likelihood][index of consequence]

risk_matrix = [
    [3, 4, 4, 5, 5],
    [2, 3, 3, 4, 5],
    [2, 2, 3, 3, 4],
    [1, 2, 2, 3, 4],
    [1, 1, 2, 2, 3],
]

# strip new line off end of string
# useful for parsing text from other sources
def stripNewLineOffEnd(value: Union[str, None]) -> str:
    if value and value[-1] == "\n":
        return value[:-1]
    return value

# returns the value of a key in a dictionary or
# an empty string if the key does not exist
def _(dictionary: dict, key: Union[str, None]) -> str:
    if key in dictionary:
        return dictionary[key]
    return ""

# parse all docstrings and convert them into a parseable format (dictionary)
def parseDocstringsToHazardLog() -> list[dict[str, Union[str, int]]]:
    # initialise variables
    all_hazards = []
    rows = []
    hazard_count = 0
    # get all python files
    all_python_files = glob.glob("../app/**.py", recursive=True)
    # get initial hazard log
    initial_hazard_log = yaml.safe_load(open("../app/crm/initial_hazard_log.yaml"))

    for file in (all_python_files):
        with open(file, "r") as source:
            # parse file
            tree = ast.parse(source.read())

        # get docstring for each function
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.FunctionDef)
                or isinstance(node, ast.AsyncFunctionDef)
                or isinstance(node, ast.ClassDef)
            ):
                docstring = ast.get_docstring(node)
                if docstring is None:
                    # if no docstring
                    continue
                # get pointers to start and end of hazards
                begin_index = docstring.find(start_indicator)
                end_index = docstring.find(end_indicator)
                if begin_index == -1 or end_index == -1:
                    # if no hazards
                    continue
                # pull out hazards from docstring
                hazards = docstring[begin_index + len(start_indicator) : end_index]
                # parse all hazards in docstring
                for hazard in yaml.safe_load(hazards)["hazards"]:
                    all_hazards.append(hazard)

    # parse initial hazard log
    order = 0
    # add initial hazards to list of hazards
    # the order is set so initial hazards are at the top of the list,
    # while the order of the initial hazard log is preserved
    for hazard in initial_hazard_log["hazards"]:
        all_hazards.insert(order, hazard)
        order += 1

    # iterating over all hazards
    for hazard in all_hazards:
        # increment hazard count to calculate hazard id
        hazard_count += 1
        # set hazard id from template in config
        hazard["id"] = config["hazard_id_template"].format(hazard_count)
        for cause in hazard["causes"]:
            # set cause id from template in config
            cause["id"] = config["cause_id_template"].format(
                hazard_count, hazard["causes"].index(cause) + 1
            )
            for control in cause["controls"]:
                # set control id from template in config
                control["id"] = config["control_id_template"].format(
                    hazard_count,
                    hazard["causes"].index(cause) + 1,
                    cause["controls"].index(control) + 1,
                )
                # if control has no initial likelihood or consequence
                # throw - they are required
                if control["initial_likelihood"] not in valid_likelihoods:
                    raise Exception(
                        "Invalid likelihood:", control["initial_likelihood"])
                if control["initial_consequence"] not in valid_severities:
                    raise Exception(
                        "Invalid consequence:", control["initial_consequence"])

                if control["residual_likelihood"] not in valid_likelihoods:
                    raise Exception(
                        "Invalid likelihood:", control["residual_likelihood"])
                if control["residual_consequence"] not in valid_severities:
                    raise Exception(
                        "Invalid consequence:", control["residual_consequence"])

                # set initial and residual risk from risk matrix
                control["initial_risk"] = risk_matrix[
                    valid_likelihoods.index(control["initial_likelihood"])
                ][valid_severities.index(control["initial_consequence"])]

                control["residual_risk"] = risk_matrix[
                    valid_likelihoods.index(control["residual_likelihood"])
                ][valid_severities.index(control["residual_consequence"])]

                # form the row for the hazard log
                rows.append(
                    {
                        "hazard_id": hazard["id"],
                        "hazard_name": stripNewLineOffEnd(_(hazard, "name")),
                        "clinical_impact": stripNewLineOffEnd(
                            _(hazard, "clinical_impact")),
                        "cause_id": cause["id"],
                        "cause": stripNewLineOffEnd(_(cause, "cause")),
                        "control_id": control["id"],
                        "initial_sofware_design": stripNewLineOffEnd(
                            _(control, "initial_sofware_design")),
                        "initial_training_communication": stripNewLineOffEnd(
                            _(control, "initial_training_communication")),
                        "initial_business_process": stripNewLineOffEnd(
                            _(control, "initial_business_process")),
                        "initial_consequence": _(control, "initial_consequence"),
                        "initial_likelihood": _(control, "initial_likelihood"),
                        "initial_risk": _(control, "initial_risk"),
                        "residual_software_design": stripNewLineOffEnd(
                            _(control, "residual_sofware_design")),
                        "residual_training_communication": stripNewLineOffEnd(
                            _(control, "residual_training_communication")),
                        "residual_business_process": stripNewLineOffEnd(
                            _(control, "residual_business_process")),
                        "residual_likelihood": _(control, "residual_likelihood"),
                        "residual_consequence": _(control, "residual_consequence"),
                        "residual_risk": _(control, "residual_risk"),
                        "tag": _(control, "tag")
                    }
                )
    # return the hazard log
    return rows
    