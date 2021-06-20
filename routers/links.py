from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List

from models.links import Links
from services.links import postPropertyLink, deletePropertyLink


router = APIRouter()

@router.post("/property/{propertyId}/link", response_description="Add new link to property", response_model=Links)
def create_link(propertyId: str, link: Links):
    link = jsonable_encoder(link)
    links = postPropertyLink(propertyId, link)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=links)


@router.delete("/property/{propertyId}/link/{id}", response_description="Delete link")
def delete_link(id: str, propertyId: str):

    links = deletePropertyLink(id, propertyId)

    if links is not None:
        return links

    raise HTTPException(status_code=404, detail=f"Link {id} not found")
