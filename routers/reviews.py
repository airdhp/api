from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from models.reviews import Reviews
from services.reviews import postPropertyReview, deletePropertyReview

router = APIRouter()

@router.post("/property/{propertyId}/review", response_description="Add new review to property", response_model=Reviews)
def create_review(propertyId: str, review: Reviews):
    review = jsonable_encoder(review)
    reviews = postPropertyReview(propertyId, review)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=reviews)


@router.delete("/property/{propertyId}/review/{id}", response_description="Delete review")
def delete_review(id: str, propertyId: str):

    reviews = deletePropertyReview(id, propertyId)

    if reviews is not None:
        return reviews

    raise HTTPException(status_code=404, detail=f"Review {id} not found")
