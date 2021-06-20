import os
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
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

conf = ConnectionConfig(
   MAIL_USERNAME=os.environ['EMAIL_USERNAME'],
   MAIL_PASSWORD=os.environ['EMAIL_PASSWD'],
   MAIL_FROM = os.environ['EMAIL_USERNAME'],
   MAIL_PORT=587,
   MAIL_SERVER="smtp.gmail.com",
   MAIL_TLS=True,
   MAIL_SSL=False,
   MAIL_DEBUG=1,
   USE_CREDENTIALS = True
)

def sendEmail(notification):

    notification['createdAt'] = current_time
    notification['updatedAt'] = current_time
    notification['channel'] = 'email'
    notification['template'] = "<html><body>" + notification['message'] + "</body></html>"

    update_result = db["notifications"].insert_one(notification)

    return notification
