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


def postPropertyReview(propertyId, review):
    review['createdAt'] = current_time
    review['updatedAt'] = current_time
    review['propertyId'] = propertyId
    update_result = db["reviews"].insert_one(review)
    result = db["reviews"].find_one({ "_id": update_result.inserted_id })
    return result

def getHighlightedReviews():
    reviews = list(db["reviews"].find({ "highlighted": True, "active": True }))
    result = []
    for r in reviews:
        r['photoUrl'] = getRandomPropertyPhoto(r['propertyId'])
        result.append(r)
    return result

def getRandomPropertyPhoto(propertyId):
    result = ""
    count = db["photos"].find({"propertyId": propertyId, "active": True }).count()
    if count > 0:
        result = db["photos"].find_one({"propertyId": propertyId, "active": True })
        random = result['imageUrl']['secure_url']
    return random

def deletePropertyReview(id, propertyId):
    update_result = db["reviews"].update_one({"_id": id }, { "$set": { "active": False, "updatedAt": current_time }})
    return {}
