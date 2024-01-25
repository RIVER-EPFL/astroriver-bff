from typing import Any
from fastapi import Depends, APIRouter, Query, Response, Body
from app.config import config
from app.utils import get_async_client
import httpx
from uuid import UUID
from app.models.user import User
from app.auth import require_admin, get_user_info

router = APIRouter()


@router.get("/{device_id}")
async def get_astrocast_device(
    client: httpx.AsyncClient = Depends(get_async_client),
    *,
    device_id: UUID,
    user: User = Depends(get_user_info),
) -> Any:
    """Get an individual astrocast device record by its local id"""

    res = await client.get(
        f"{config.RIVER_API_URL}/v1/astrocast/devices/{device_id}",
    )

    return res.json()


@router.get("")
async def get_all_astrocast_devices(
    response: Response,
    *,
    filter: str = Query(None),
    sort: str = Query(None),
    range: str = Query(None),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(get_user_info),
) -> Any:
    """Get all astrocast devices"""

    res = await client.get(
        f"{config.RIVER_API_URL}/v1/astrocast/devices/",
        params={"sort": sort, "range": range, "filter": filter},
    )
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = res.headers["Content-Range"]

    return res.json()
