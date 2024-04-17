from app.config import config
from sqlmodel_react_admin.routers import ReactAdminBFFRouter


sensor_parameters = ReactAdminBFFRouter(
    name_singular="sensor parameter",
    prefix="/sensor_parameters",
    base_url=f"{config.RIVER_API_URL}/v1",
)
