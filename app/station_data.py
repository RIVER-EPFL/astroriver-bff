from typing import Any
from fastapi import Depends, APIRouter, Query, Response, Body
from app.config import config
from app.utils import get_async_client
import httpx
from uuid import UUID
from app.models.user import User
from app.auth import require_admin, get_user_info
from sqlmodel_react_admin.routers import ReactAdminBFFRouter

router = APIRouter()


station_data = ReactAdminBFFRouter(
    name_singular="data",
    name_plural="data",
    prefix="/station_data",
    base_url=f"{config.RIVER_API_URL}/v1/stations",
)
