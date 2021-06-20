import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List

load_dotenv()
current_time = datetime.now().isoformat(timespec='microseconds')

client = MongoClient(os.environ['MONGODB_CONNECTION'])
db = client.db

env = os.getenv('ENV')

cloudinary.config(cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), api_key=os.getenv('CLOUDINARY_API_KEY'), api_secret=os.getenv('CLOUDINARY_API_SECRET'))


def postPropertyPhoto(propertyId, file):

    upload_result = cloudinary.uploader.upload(file, folder="/" + env + "/images/")
    count = db["photos"].find({ "propertyId": propertyId, "active": True }).count()

    photo = {}
    photo['_id'] = str(ObjectId())
    photo['createdAt'] = current_time
    photo['updatedAt'] = current_time
    photo['propertyId'] = propertyId
    photo['imageUrl'] = {}
    photo['imageUrl']['url'] = upload_result['url']
    photo['imageUrl']['secure_url'] = upload_result['secure_url']
    photo['active'] = True
    photo['isMain'] = False
    photo['order'] = count+1

    update_result = db["photos"].insert_one(photo)

    photos = list(db["photos"].find({ "propertyId": propertyId, "active": True }))
    return photos


def photoReorder(propertyId):
    photos = db["photos"].find({"propertyId": propertyId, "active": True}).sort("order")
    i=1
    print(photos)
    for photo in photos:
        update = db["photos"].update_one({"_id": photo['_id']}, { "$set": { "order": i }})
        i+=1


def deletePropertyPhoto(id, propertyId):
    update_result = db["photos"].update_one({"_id": id }, { "$set": { "active": False, "updatedAt": current_time }})
    photoReorder(propertyId)
    photos = list(db["photos"].find({ "propertyId": propertyId, "active": True }))
    return photos


def getPhoto(id):
    result = db["photos"].find_one({"_id": id })
    return result
