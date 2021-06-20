from fastapi import APIRouter, File, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from models.photos import Photos
from services.photos import postPropertyPhoto, deletePropertyPhoto

router = APIRouter()

@router.post("/property/{propertyId}/photo", response_description="Add new photo to property")
async def create_photo(propertyId: str, file: bytes = File(...)):

    photos = postPropertyPhoto(propertyId, file)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=photos)

@router.delete("/property/{propertyId}/photo/{id}", response_description="Delete photo")
def delete_photo(propertyId: str, id: str):

    photos = deletePropertyPhoto(id, propertyId)
    if photos is not None:
        return photos

    raise HTTPException(status_code=404, detail=f"Photo {id} not found")
