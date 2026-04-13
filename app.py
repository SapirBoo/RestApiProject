
from contextlib import asynccontextmanager

from fastapi import FastAPI
import sqlalchemy 
from db import Base,engine
import os

from models import item, tag, itams_tags
from resources.store import rt as store_router
from resources.item import rt as item_router
from resources.tag import rt as tag_router
from routers.auth import rt as auth_router
from resources.user import rt as user_router 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic
    #Base.metadata.create_all(bind=engine)
    
    yield
        
#----Create APP ----
def create_app():
    app = FastAPI(
        title="My API",
        version="1.0.0",
        openapi_url="/api/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan= lifespan 
    )
    
    
    
    app.include_router(store_router)
    app.include_router(item_router)
    app.include_router(tag_router)
    app.include_router(auth_router)
    app.include_router(user_router)
    return app


app = create_app()
