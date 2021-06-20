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

def getProperties():
    properties = list(db["properties"].find({"active": True}).sort("order"))
    return properties

def getPropertyBySlug(slug):
    id = db["properties"].find_one({"slug": slug})['_id']
    id = getProperty(id)['_id']
    property = getResponsePropertyModel(id)
    return property

def getPropertiesFull():
    properties = list(db["properties"].find({"active": True}).sort("order"))
    result = []
    for p in properties:
        result.append(getResponsePropertyModel(p['_id']))
    return result

def getProperty(id):
    property = db["properties"].find_one({"_id": id})
    return property

def postProperty(property):
    count = db["properties"].find({ "active": True }).count()

    property['order'] = count+1
    property['createdAt'] = current_time
    property['updatedAt'] = current_time

    new_property = db["properties"].insert_one(property)
    created_property = getResponsePropertyModel(id=new_property.inserted_id)
    return created_property

def putProperty(id, property):
    property['updatedAt'] = current_time
    update_result = db["properties"].update_one({"_id": id}, {"$set": property})
    property = getProperty(id)
    return property

def deleteProperty(id):
    if db["properties"].find({"_id": id, "active": True}).count() > 0:
        result = db["properties"].update_one({"_id": id}, { "$set": { "active": False, "updatedAt": current_time }})
        propertiesReorder()
        return {}
    else:
        return None


def propertiesReorder():
    properties = db["properties"].find({ "active": True}).sort("order")
    i=1
    for property in properties:
        update = db["properties"].update_one({"_id": property['_id']}, { "$set": { "order": i }})
        i+=1


def getResponsePropertyModel(id):
    property = db["properties"].find_one({"_id": id})
    if db["photos"].find({"propertyId": id, "active": True}).count() > 0:
        property["photos"] = list(db["photos"].find({"propertyId": id, "active": True}).sort("order"))
    else:
        property["photos"] = []

    if db["reviews"].find({"propertyId": id, "active": True}).count() > 0:
        property["reviews"] = list(db["reviews"].find({"propertyId": id, "active": True}))
    else:
        property["reviews"] = []

    if db["links"].find({"propertyId": id, "active": True}).count() > 0:
        property["links"] = list(db["links"].find({"propertyId": id, "active": True}))
    else:
        property["links"] = []

    return property
