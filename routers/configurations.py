from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List

from models.configurations import Configuration
from services.configurations import postConfiguration, getConfiguration


router = APIRouter()

@router.post("/configuration", response_description="Add new configuration", response_model=Configuration)
def create_configuration(config: Configuration):
    config = jsonable_encoder(config)
    configs = postConfiguration(config)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=configs)


@router.get("/configuration", response_description="Get Website configuration", response_model=Configuration)
def get_configuration():

    config = getConfiguration()

    if config is not None:
        return config
    else:
        return {}
