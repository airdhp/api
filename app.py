from fastapi import FastAPI, Body, HTTPException, status, File, UploadFile, Header, APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware

from dependencies import verify_api_token, verify_admin_token
from routers import properties, photos, reviews, links, internal, website, configurations

middleware = [ Middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*']))]

app = FastAPI(middleware=middleware)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

app.include_router(properties.router,
    prefix="/console",
    tags=["properties"],
    dependencies=[Depends(verify_api_token)]
)

app.include_router(photos.router,
    prefix="/console",
    tags=["photos"],
    dependencies=[Depends(verify_api_token)]
)

app.include_router(reviews.router,
    prefix="/console",
    tags=["reviews"],
    dependencies=[Depends(verify_api_token)]
)

app.include_router(links.router,
    prefix="/console",
    tags=["links"],
    dependencies=[Depends(verify_api_token)]
)

app.include_router(website.router,
    prefix="/website",
    tags=["website"],
    dependencies=[Depends(verify_api_token)]
)

app.include_router(configurations.router,
    prefix="/console",
    tags=["config"],
    dependencies=[Depends(verify_api_token)]
)

app.include_router(internal.router,
    prefix="/console/internal",
    tags=["internal"],
    dependencies=[Depends(verify_admin_token)]
)
