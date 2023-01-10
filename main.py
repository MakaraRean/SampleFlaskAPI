import uvicorn
from fastapi import FastAPI

from app.controllers import productController
from app.dependancies import authentication

app = FastAPI()

app.include_router(authentication.app)
app.include_router(productController.app)

if __name__ == '__main__':
    uvicorn.run(app=app)
