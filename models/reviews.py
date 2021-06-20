from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Reviews(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    propertyId: Optional[str] = None
    date: Optional[str] = None
    source: Optional[str] = None
    author: Optional[str] = None
    review: str
    highlighted: bool
    active: bool
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
