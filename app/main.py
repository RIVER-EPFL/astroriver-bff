from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from app.config import config
from app.models.config import KeycloakConfig
from app.models.health import HealthCheck
from app.areas import router as areas_router
from app.stations import router as stations_router
from app.sensordata import router as sensordata_router
from app.users import router as users_router
from app.astrocast_messages import router as astrocast_message_router
from app.astrocast_devices import router as astrocast_device_router
from app.station_sensors import router as station_sensor_router
from app.sensors import router as sensor_router
from app.station_data import station_data
from app.sensor_parameters import sensor_parameters

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(f"{config.API_PREFIX}/config/keycloak")
async def get_keycloak_config() -> KeycloakConfig:
    return KeycloakConfig(
        clientId=config.KEYCLOAK_CLIENT_ID,
        realm=config.KEYCLOAK_REALM,
        url=config.KEYCLOAK_URL,
    )


@app.get(
    "/healthz",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """Perform a Health Check

    Useful for Kubernetes to check liveness and readiness probes
    """
    return HealthCheck(status="OK")


app.include_router(
    areas_router,
    prefix=f"{config.API_PREFIX}/areas",
    tags=["areas"],
)
app.include_router(
    stations_router,
    prefix=f"{config.API_PREFIX}/stations",
    tags=["sensors"],
)
app.include_router(
    sensordata_router,
    prefix=f"{config.API_PREFIX}/sensordata",
    tags=["sensordata"],
)
app.include_router(
    astrocast_message_router,
    prefix=f"{config.API_PREFIX}/astrocast_messages",
    tags=["astrocast", "messages"],
)
app.include_router(
    astrocast_device_router,
    prefix=f"{config.API_PREFIX}/astrocast_devices",
    tags=["astrocast", "devices"],
)
app.include_router(
    users_router,
    prefix=f"{config.API_PREFIX}/users",
    tags=["users"],
)
app.include_router(
    sensor_router,
    prefix=f"{config.API_PREFIX}/sensors",
    tags=["sensors", "devices"],
)
app.include_router(
    station_sensor_router,
    prefix=f"{config.API_PREFIX}/station_sensors",
    tags=["sensors", "stations"],
)
app.include_router(  # Use abstracted router from sqlmodel-react-admin
    station_data.router,
    prefix=f"{config.API_PREFIX}{station_data.prefix}",
    tags=["station_data"],
)
app.include_router(
    sensor_parameters.router,
    prefix=f"{config.API_PREFIX}/sensor_parameters",
    tags=["sensor_parameters"],
)
