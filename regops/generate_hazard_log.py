import yaml
import pandas as pd
import shutil
import datetime
import asyncio
from versioning import setDocumentVersion, getIncrementedVersion
from parse_docstrings import parseDocstringsToHazardLog

# get incremented version number
new_version = asyncio.run(getIncrementedVersion(increase_minor=True))

# load config from yaml
config = yaml.safe_load(open("regops_config.yaml"))["regops"]

# set replacements (what in template will be replaced with what)
replacements = {
    "APPLICATION_NAME": config["application_name"],
    "OWNER": config["owner"],
    "AUTHORS": config["authors"],
}

# Get output file name and path
output_file_name = str(config["output_name_template"]).format(
    new_version[0], new_version[1]
)
output_file_path = f"{config['output_folder']}/{output_file_name}"

# Copy template to output file
shutil.copyfile(config['xlsx_template'], output_file_path)

# Parse docstrings into dataframe
df = pd.DataFrame(parseDocstringsToHazardLog())

# Create dataframes for information and application title
info_df = pd.DataFrame(
    [
        replacements["OWNER"],
        replacements["AUTHORS"],
        config["version_template"].format(new_version[0], new_version[1]),
        datetime.datetime.now().strftime("%d/%m/%Y"),
        "One year from last significant change",
    ]
)
app_title_df = pd.DataFrame([replacements["APPLICATION_NAME"]])

# Initialise writer and configure data to overlay template
with pd.ExcelWriter(output_file_path, mode="a", if_sheet_exists="overlay") as writer:
    # Write each dataframe to the template
    df.to_excel(writer, "Hazard log", startrow=2, startcol=0, index=False, header=False)
    info_df.to_excel(
        writer, "Information", startrow=3, startcol=2, index=False, header=False
    )
    app_title_df.to_excel(
        writer, "Information", startrow=1, startcol=1, index=False, header=False
    )

# Set new document version in database
asyncio.run(
    setDocumentVersion(new_version=new_version))
