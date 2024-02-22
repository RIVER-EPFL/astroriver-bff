from typing import Any
from fastapi import Depends, APIRouter, Query, Response, Body
from app.config import config
from app.utils import get_async_client
import httpx
from uuid import UUID
from app.models.user import User
from app.auth import require_admin, get_user_info

router = APIRouter()


@router.get("/{station_id}/{sensor_position}")
async def get_station_sensor_by_position(
    client: httpx.AsyncClient = Depends(get_async_client),
    *,
    station_id: UUID,
    sensor_position: int,
    user: User = Depends(get_user_info),
) -> Any:
    """Get a station sensor by station ID and sensor position"""

    res = await client.get(
        f"{config.RIVER_API_URL}/v1/"
        f"stations/sensors/{station_id}/{sensor_position}",
    )

    return res.json()


@router.get("/{station_sensor_id}")
async def get_station_sensor(
    client: httpx.AsyncClient = Depends(get_async_client),
    *,
    station_sensor_id: UUID,
    user: User = Depends(get_user_info),
) -> Any:
    """Get a station sensor by station-sensor ID"""

    res = await client.get(
        f"{config.RIVER_API_URL}/v1/stations/sensors/{station_sensor_id}",
    )

    return res.json()


@router.get("")
async def get_stations(
    response: Response,
    *,
    filter: str = Query(None),
    sort: str = Query(None),
    range: str = Query(None),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(get_user_info),
) -> Any:
    """Get all station sensors"""

    res = await client.get(
        f"{config.RIVER_API_URL}/v1/stations/sensors",
        params={"sort": sort, "range": range, "filter": filter},
    )
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = res.headers["Content-Range"]

    return res.json()


@router.post("")
async def create_station_sensor_mapping(
    station_sensor: Any = Body(...),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> Any:
    """Creates a station-sensor mapping"""

    res = await client.post(
        f"{config.RIVER_API_URL}/v1/stations/sensors",
        json=station_sensor,
    )

    return res.json()


@router.put("/{station_sensor_id}")
async def update_station_sensor_mapping(
    station_sensor_id: UUID,
    station_sensor: Any = Body(...),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> Any:
    """Sets a station sensor mapping"""

    res = await client.put(
        f"{config.RIVER_API_URL}/v1/" f"stations/sensors/{station_sensor_id}",
        json=station_sensor,
    )

    return res.json()


@router.delete("/{station_sensor_id}")
async def delete_station(
    station_sensor_id: UUID,
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> None:
    """Remove a station sensor mapping by station id and sensor position"""

    res = await client.delete(
        f"{config.RIVER_API_URL}/v1/" f"stations/sensors/{station_sensor_id}",
    )

    return res.json()
