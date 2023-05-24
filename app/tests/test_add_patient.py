from httpx import Response


async def test_add_patient(httpx_test_client) -> None:
    res: Response = await httpx_test_client.post(
        "/patient/",
        json={
            "nhs_number": "1234567890",
            "mrn": "1234567890",
            "first_name": "John",
            "last_name": "Smith",
            "date_of_birth": "2021-01-01",
        },
    )
    assert res.status_code == 200
    assert res.json() == {"status": "success"}
