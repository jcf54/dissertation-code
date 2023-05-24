from datetime import date
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from enum import Enum

app = FastAPI(debug=True)


class AddPatientInput(BaseModel):
    """
    Used as a dataclass for putting
    patients into the system
    """

    nhs_number: str
    mrn: str
    first_name: str
    last_name: str
    date_of_birth: date


@app.post("/patient/")
async def add_patient(patient_data: AddPatientInput) -> JSONResponse:
    """
    Parameters:
    nhs_number: str
    mrn: str
    first_name: str
    last_name: str
    date_of_birth: date

    Returns:
    JSONResponse

    -----BEGIN HAZARDS-----
    hazards:
    - name: Patient added into system twice
      clinical_impact: >
        Potential for conflicting information leading to bad decision making
      causes:
        - cause: Identifer entered incorrectly
          controls:
            - initial_consequence: Considerable
              initial_likelihood: Medium
              residual_consequence: Minor
              residual_likelihood: Low
              residual_sofware_design: >
                Check if the patient exists in the
                system by other information
              tag: DCB0129
            - initial_consequence: Considerable
              initial_likelihood: Medium
              residual_consequence: Minor
              residual_likelihood: Low
              residual_sofware_design: >
                Display a verification modal so the user can confirm the new
                patient's details
              tag: DCB0129
    - name: Patient added into system with incorrect details
      clinical_impact: >
        The patient may be misidentified in the future, or
        may not be identified at all leading to poor decision
        making
      causes:
        - cause: Identifer entered incorrectly
          controls:
            - initial_consequence: Considerable
              initial_likelihood: Medium
              residual_consequence: Minor
              residual_likelihood: Low
              residual_sofware_design: >
                Display a verification modal so the user can confirm the new
                patient's details
              tag: DCB0129
    -----END HAZARDS-----
    """

    # logic to add patient into database would go here

    return JSONResponse({"status": "success"})


class ScanTypes(str, Enum):
    CT = "CT"
    MRI = "MRI"
    XRAY = "XRAY"


class ScanRequestInput(BaseModel):
    """
    Used as a dataclass for archiving
    patients in the system
    """

    patient_id: int
    scan_type: ScanTypes


@app.post("/patient/scan/")
async def request_ct_scan(scan_request: ScanRequestInput) -> JSONResponse:
    """
    Parameters:
    patient_id: int
    scan_type: ScanTypes

    Returns:
    JSONResponse

    -----BEGIN HAZARDS-----
    hazards:
    - name: The wrong scan is requested for the patient
      clinical_impact: >
        Patient may be exposed to unnecessary radiation,
        waste of resources, patient may experience
        psychological distress if they are expecting a
        different scan
      causes:
        - cause: Identifer entered incorrectly
          controls:
            - initial_consequence: Considerable
              initial_likelihood: Medium
              residual_software_design: >
                Display a verification modal so the user can confirm the
                patient's details
              residual_training_communication: >
                Train staff to check the patient's details before requesting
                a scan
              residual_consequence: Minor
              residual_likelihood: Low
              tag: DCB0129
    - name: A patient has a scan requested for them twice
      clinical_impact: >
        Patient may be exposed to unnecessary radiation,
        waste of resources, patient may experience
        psychological distress if they are only
        expecting one scan
      causes:
        - cause: Identifer entered incorrectly
          controls:
            - initial_consequence: Considerable
              initial_likelihood: Medium
              residual_software_design: >
                Display a verification modal so the user can confirm the
                patient's details
              residual_training_communication: >
                Train staff to check the patient's details before requesting
                a scan
              residual_consequence: Minor
              residual_likelihood: Low
              tag: DCB0129
        - cause: >
            Clinician may not be aware that the patient has already had a scan
            requested for them
          controls:
            - initial_consequence: Considerable
              initial_likelihood: Medium
              residual_software_design: >
                Display previous and outstanding scan requests for the patient
              residual_consequence: Minor
              residual_likelihood: Low
              tag: DCB0129
        - cause: >
            Clinician may not be aware that the patient has already had a scan
            requested for them
          controls:
            - initial_consequence: Considerable
              initial_likelihood: Medium
              residual_software_design: >
                Do not allow clinicians to request scans for patients who
                already have a scan requested for them within a certain time
                period
              residual_consequence: Minor
              residual_likelihood: Low
              tag: DCB0129
    -----END HAZARDS-----
    """

    # Logic to send the scan request to the PACS system would go here

    return JSONResponse({"status": "success"})


@app.post("/patient/test/")
async def test_patient(patient_id: int) -> JSONResponse:
    return JSONResponse({"status": "success"})
