from typing import Any
from fastapi import Depends, APIRouter, Query, Response, Body
from app.config import config
from app.utils import get_async_client
import httpx
from uuid import UUID
from app.models.user import User
from app.auth import require_admin, get_user_info

router = APIRouter()


@router.get("/{sensor_id}")
async def get_sensor(
    client: httpx.AsyncClient = Depends(get_async_client),
    *,
    sensor_id: UUID,
    user: User = Depends(get_user_info),
) -> Any:
    """Get a sensor by id"""

    res = await client.get(
        f"{config.RIVER_API_URL}/v1/sensors/{sensor_id}",
    )

    return res.json()


@router.get("")
async def get_sensors(
    response: Response,
    *,
    filter: str = Query(None),
    sort: str = Query(None),
    range: str = Query(None),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(get_user_info),
) -> Any:
    """Get all sensors"""

    res = await client.get(
        f"{config.RIVER_API_URL}/v1/sensors",
        params={"sort": sort, "range": range, "filter": filter},
    )
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = res.headers["Content-Range"]

    return res.json()


@router.post("")
async def create_sensor(
    sensor: Any = Body(...),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> Any:
    """Creates a sensor"""

    res = await client.post(
        f"{config.RIVER_API_URL}/v1/sensors",
        json=sensor,
    )

    return res.json()


@router.put("/{sensor_id}")
async def update_sensor(
    sensor_id: UUID,
    sensor: Any = Body(...),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> Any:
    """ "Updates a sensor by id"""

    res = await client.put(
        f"{config.RIVER_API_URL}/v1/sensors/{sensor_id}", json=sensor
    )

    return res.json()


@router.delete("/{sensor_id}")
async def delete_sensor(
    sensor_id: UUID,
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> None:
    """Delete a sensor by id"""

    res = await client.delete(f"{config.RIVER_API_URL}/v1/sensors/{sensor_id}")

    return res.json()
