from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from models.properties import Property, ResponseProperty, Photos, Reviews
from services.properties import getProperties, getProperty, postProperty, putProperty, deleteProperty

router = APIRouter()

@router.post("/property/", response_description="Add new property", response_model=ResponseProperty)
def create_property(property: Property):
    property = jsonable_encoder(property)
    created_property = postProperty(property)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_property)

@router.get("/properties/", response_description="List all properties", response_model=List[Property])
def list_properties():
    return getProperties()


@router.get("/property/{id}", response_description="Get a single property by id", response_model=Property)
def show_property(id: str):
    property = getProperty(id)
    if property is not None:
        return property
    raise HTTPException(status_code=404, detail=f"Property {id} not found")

@router.put("/property/{id}", response_description="Update a property", response_model=Property)
def update_property(id: str, property: Property):
    property = jsonable_encoder(property)
    existing_property = putProperty(id, property)

    if existing_property is not None:
        return existing_property

    raise HTTPException(status_code=404, detail=f"Property {id} not found")


@router.delete("/property/{id}", response_description="Delete property")
def delete_property(id: str):

    property = deleteProperty(id)
    if property is not None:
        return property

    raise HTTPException(status_code=404, detail=f"Property {id} not found")
