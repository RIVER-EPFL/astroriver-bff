from typing import Any
from fastapi import Depends, APIRouter, Query, Response, Body
from app.config import config
from app.utils import get_async_client
import httpx
from uuid import UUID
from app.models.user import User
from app.auth import require_admin, get_user_info

router = APIRouter()


@router.get("/{sensor_parameter_id}")
async def get_sensor_parameter(
    client: httpx.AsyncClient = Depends(get_async_client),
    *,
    sensor_parameter_id: UUID,
    user: User = Depends(get_user_info),
) -> Any:
    """Get a sensor_parameter by id"""

    res = await client.get(
        f"{config.RIVER_API_URL}/v1/sensor_parameters/{sensor_parameter_id}",
    )

    return res.json()


@router.get("")
async def get_sensor_parameters(
    response: Response,
    *,
    filter: str = Query(None),
    sort: str = Query(None),
    range: str = Query(None),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(get_user_info),
) -> Any:
    """Get all sensor devices"""

    res = await client.get(
        f"{config.RIVER_API_URL}/v1/sensor_parameters",
        params={"sort": sort, "range": range, "filter": filter},
    )
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = res.headers["Content-Range"]

    return res.json()


@router.post("")
async def create_sensor_parameter(
    sensor_parameter: Any = Body(...),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> Any:
    """Creates a sensor device"""

    res = await client.post(
        f"{config.RIVER_API_URL}/v1/sensor_parameters",
        json=sensor_parameter,
    )

    return res.json()


@router.put("/{sensor_parameter_id}")
async def update_sensor_parameter(
    sensor_parameter_id: UUID,
    sensor_parameter: Any = Body(...),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> Any:
    """Updates a sensor device by id"""

    res = await client.put(
        f"{config.RIVER_API_URL}/v1/sensor_parameters/{sensor_parameter_id}",
        json=sensor_parameter,
    )

    return res.json()


@router.delete("/{sensor_parameter_id}")
async def delete_sensor_parameter(
    sensor_parameter_id: UUID,
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> None:
    """Delete a sensor device by id"""

    res = await client.delete(
        f"{config.RIVER_API_URL}/v1/sensor_parameters/{sensor_parameter_id}"
    )

    return res.json()
