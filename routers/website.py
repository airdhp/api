import os
from fastapi import APIRouter
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import Optional, List

from models.notifications import Notification

from services.website import getWebsiteConfiguration
from services.properties import getPropertiesFull, getPropertyBySlug
from services.reviews import getHighlightedReviews
from services.email import sendEmail

load_dotenv()

conf = ConnectionConfig(
   MAIL_USERNAME=os.environ['EMAIL_USERNAME'],
   MAIL_PASSWORD=os.environ['EMAIL_PASSWD'],
   MAIL_FROM = os.environ['EMAIL_USERNAME'],
   MAIL_PORT=587,
   MAIL_SERVER="smtp.gmail.com",
   MAIL_TLS=True,
   MAIL_SSL=False,
   USE_CREDENTIALS = True
)

router = APIRouter()

router.add_middleware(
    CORSMiddleware,
    allow_origins=["https://airdhp-web.herokuapp.com", "https://airdhp-web.herokuapp.com", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@router.get("/configuration", response_description="Get Website configuration")
def get_configuration():

    config = getWebsiteConfiguration()

    if config is not None:
        return config
    else:
        return {}


@router.get("/properties", response_description="Get Properties details")
def get_properties():

    result = getPropertiesFull()

    if result is not None:
        return result
    else:
        return {}


@router.get("/property/{slug}", response_description="Get a single property by slug")
def show_property_by_slug(slug: str):
    property = getPropertyBySlug(slug)
    if property is not None:
        return property
    raise HTTPException(status_code=404, detail=f"Property {slug} not found")


@router.get("/reviews", response_description="Reviews for homepage")
def show_reviews():
    reviews = getHighlightedReviews()
    if reviews is not None:
        return reviews
    raise HTTPException(status_code=404, detail=f"Reviews for homepage not found")


@router.post("/notification", response_description="Send notification")
async def send_notification(notification: Notification):

    notification = jsonable_encoder(notification)

    if (notification['channel'] == "email"):
        notification = sendEmail(notification)

        message = MessageSchema(
            subject=notification['subject'],
            recipients=[notification['receiver']],  # List of recipients, as many as you can pass
            body=notification['template'],
            subtype="html"
        )

        fm = FastMail(conf)
        await fm.send_message(message)

        return JSONResponse(status_code=200, content={'result': 'success', 'msg': 'Notification has been sent.'})
    return JSONResponse(status_code=400, content={'result': 'error', 'msg': 'Bad request. Channel not defined or incorrect.'})
