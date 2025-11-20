from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.clients.otp_client import OtpClient, OtpClientError
from app.schemas.isochrone import IsochroneQuery

router = APIRouter(prefix="/api", tags=["isochrone"])


def get_otp_client(request: Request) -> OtpClient:
    client: OtpClient = request.app.state.otp_client
    return client


@router.get("/isochrone")
async def read_isochrone(
    params: IsochroneQuery = Depends(),
    otp_client: OtpClient = Depends(get_otp_client),
):
    try:
        data = await otp_client.fetch_isochrone(params)
        return data
    except OtpClientError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.message,
        ) from exc

