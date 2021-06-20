from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from models.photos import Photos
from models.reviews import Reviews
from models.links import Links


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

class Locations(BaseModel):
    name: str
    lat: float
    lng: float

class Attributes(BaseModel):
    type: str
    value: int

class Extras(BaseModel):
    type: str
    value: bool

class Property(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    landlordCode: str
    propertyType: str
    slug: str
    title: str
    summary: str
    desc: Optional[str] = None
    location: Locations
    attributes: List[Attributes]
    extras: Optional[List[Extras]] = None
    order: Optional[int] = None
    active: bool
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ResponseProperty(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    code: str
    landlordCode: str
    propertyType: str
    slug: str
    title: str
    summary: str
    desc: Optional[str] = None
    location: Locations
    attributes: List[Attributes]
    extras: Optional[List[Extras]] = None
    photos: Optional[List[Photos]] = None
    reviews: Optional[List[Reviews]] = None
    links: Optional[List[Links]] = None
    order: Optional[int] = None
    active: bool
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
