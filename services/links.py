import os
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


def postPropertyLink(propertyId, link):
    link['createdAt'] = current_time
    link['updatedAt'] = current_time
    link['propertyId'] = propertyId
    update_result = db["links"].insert_one(link)
    links = list(db["links"].find({ "propertyId": propertyId, "active": True }))
    return links

def getLink(id):
    result = db["links"].find({ "_id": id })
    return result

def deletePropertyLink(id, propertyId):
    update_result = db["links"].update_one({"_id": id }, { "$set": { "active": False, "updatedAt": current_time }})
    links = list(db["links"].find({ "propertyId": propertyId, "active": True }))
    return links
