import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
import random
import string

load_dotenv()
current_time = datetime.now().isoformat(timespec='microseconds')

client = MongoClient(os.environ['MONGODB_CONNECTION'])
db = client.db

def randStr(chars = string.ascii_uppercase + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))

def postApiclient(client):
    client['createdAt'] = current_time
    client['updatedAt'] = current_time
    client['api_key'] = randStr(N=20)
    client['api_secret'] = randStr(N=20)
    update_result = db["apiclients"].insert_one(client)

    result = db["apiclients"].find_one({ "_id": update_result.inserted_id })
    return result

def getApiclients():
    results = list(db["apiclients"].find())
    return results

def deleteApiclient(id):
    update_result = db["apiclients"].update_one({"_id": id }, { "$set": { "active": False, "updatedAt": current_time }})
    return {}

def verifyApiCredentials(api_key, api_secret):
    if db["apiclients"].find({ "api_key": api_key, "api_secret": api_secret, "active": True }).count() > 0:
        return True
    else:
        return False
