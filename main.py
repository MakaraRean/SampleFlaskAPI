import datetime
from typing import Union

import uvicorn
from fastapi import FastAPI
from flask import request
from pydantic import BaseModel

from app.controllers import productController
from app.dependancies import authentication
from database import Session
from app.models.models import Product

app = FastAPI()

app.include_router(authentication.app)
app.include_router(productController.app)

if __name__ == '__main__':
    uvicorn.run(app=app, debug=True)
