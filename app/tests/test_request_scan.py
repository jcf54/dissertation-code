from httpx import Response
from ..api import ScanTypes


async def test_request_scan(httpx_test_client) -> None:
    res: Response = await httpx_test_client.post(
        "/patient/scan/",
        json={
            "patient_id": "9999999",
            "scan_type": ScanTypes.CT,
        },
    )
    assert res.status_code == 200
    assert res.json() == {"status": "success"}
