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

def postConfiguration(config):

    if db["configurations"].find({"active": True}).count() > 0:
        get_current = db["configurations"].find({"active": True}).limit(1).sort([('$natural',-1)])
        update_result = db["configurations"].update_one({"_id": get_current[0]['_id'] }, { "$set": { "active": False, "updatedAt": current_time }})

    config['createdAt'] = current_time
    config['updatedAt'] = current_time
    config['active'] = True

    update_result = db["configurations"].insert_one(config)

    result = db["configurations"].find_one({ "_id": update_result.inserted_id })
    return result

def getConfiguration():
    results = db["configurations"].find({"active": True}).limit(1).sort([('$natural',-1)])
    return results[0]
