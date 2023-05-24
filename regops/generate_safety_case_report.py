from parse_docstrings import parseDocstringsToHazardLog
from parse_requirements import parseRequirements
import yaml

# load third party services from yaml
third_party_services = yaml.safe_load(
    open("../app/crm/third_party_services.yaml"))

# load requirements
requirements: dict[str, dict] = parseRequirements()


# read the template
template_contents = ""
with open("templates/clinical_safety_case_report_template.md", "r") as source:
    template_contents = source.read()

hazard_log_md = ""

# parse docstrings into hazard log markdown file
for hazard in parseDocstringsToHazardLog():
    control_software = ""
    control_training = ""
    control_business = ""

    if hazard["residual_software_design"]:
        control_software = f"""##### Software

{hazard['residual_software_design']}"""

    if hazard["residual_training_communication"]:
        control_training = f"""##### Training/communication

{hazard['residual_training_communication']}"""

    if hazard["residual_business_process"]:
        control_business = f"""##### Business processes

{hazard['residual_business_process']}"""

    hazard_log_md += f"""
### {hazard['hazard_name']}

#### Clinical impact

{hazard['clinical_impact']}

#### Control measures

{control_software}

{control_training}

{control_business}

#### Analysis

| Consequence | Likelihood | Risk score |
| --- | --- | --- |
| {hazard['residual_likelihood']} | {hazard['residual_consequence']} | {hazard['residual_risk']} |
"""

# replace the hazard log template with the parsed hazard log
template_contents = template_contents.replace("{HAZARD_LOG}", hazard_log_md)

requirements_section = ""

for library_name, details in requirements.items():
    requirements_section += f"""### {library_name}

[{details[0]}]({details[0]})

{details[1]}

"""
# iterate over third party services
for service in third_party_services["services"]:
    requirements_section += f"""### {service["name"]}

[{service["url"]}]({service["url"]})

{service["description"]}"""

# replace the third party tools template with the parsed third party tools
template_contents = template_contents.replace(
    "{THIRD_PARTY_TOOLS}", requirements_section)

# write the output file
with open("artifacts/clinical_safety_case_report.md", "w") as output:
    output.write(template_contents)
