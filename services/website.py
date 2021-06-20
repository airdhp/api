import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId

load_dotenv()

client = MongoClient(os.environ['MONGODB_CONNECTION'])
db = client.db

def getWebsiteConfiguration():
	results = db["configurations"].find({"active": True}).limit(1).sort([('$natural',-1)])[0]

	website_config = {}
	website_config['properties'] = results['config']['properties']
	website_config['partners'] = results['config']['partners']
	website_config['website'] = results['config']['website']

	return website_config
