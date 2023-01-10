import uvicorn
from fastapi import FastAPI,Response,status,Depends
from fastapi.security import OAuth2AuthorizationCodeBearer,HTTPBearer
from app.models.models import Product
from app.pydantic import request, productResponse
from database import Session, Base, engine
from routes.routers import product
from app.dependancies.authentication import ALGORITHM, SECTET_KEY, Token
from app.dependancies.auth import authentication as Auth

app = product
route = product
oauth2_scheme = HTTPBearer()

@app.get("/getToken",summary= "Testing OAuth2 Token",dependencies=[Depends(Auth)])
async def getToken(token: str = Depends(oauth2_scheme)):

    return {"token": token}


@ app.get("/getProduct",summary="List all product",dependencies= [Depends(Auth)])
async def getProduct(token: str = Depends(oauth2_scheme)):
    # product = Product()
    result = dict(code='000', message='SUCCESS', message_kh='ជោគជ័យ')
    #payload = jwt.decode(token,SECTET_KEY,algorithms=ALGORITHM)
    try:
        session = Session()
        products = session.query(Product).all()
        if token.credentials == Token.access_token:
            return products
        else:
            return {"message": "Token is invalid"}
    except Exception as ex:
        return {"message": f"Token invalid, {ex}"}


@app.get('/getProduct/{pid}', summary="List a product specific by product id", dependencies=[Depends(Auth)])
async def getProductById(pid: int,token: str = Depends(oauth2_scheme)):
    # pid = {"id": id}
    session = Session()
    product = session.query(Product).get(pid)

    return product


@app.post("/addProduct", summary="Create new product", dependencies=[Depends(Auth)])
async def addProduct(request: request.Product,token: str = Depends(oauth2_scheme)):
    try:
        session = Session()
        product = Product(
            name=request.name,
            qty=request.qty,
            price=request.price,
            createdAt=request.createdAt,
            category_id=request.category_id
        )
        session.add(product)
        session.commit()
        return {"success": f"Product {product.name} inserted"}
    except Exception as ex:
        return {"error": ex}


@app.put("/updateProduct/{id}",summary="Update any product specific by product id",dependencies=[Depends(Auth)])
async def updateProduct(id: int,request: request.Product,token: str = Depends(oauth2_scheme)):
    try:
        session = Session()
        pro = session.query(Product).get(id)
        # product = Product(
        #     name=request.name,
        #     qty=request.qty,
        #     price= request.price,
        #     createdAt= request.createdAt,
        #     category_id= request.category_id
        # )
        pro.name = request.name
        pro.qty = request.qty
        pro.price = request.price
        pro.createdAt = request.createdAt
        pro.category_id = request.category_id

        session.commit()
        return pro
    except Exception as ex:
        return ex

@app.delete("/deleteProduct/{id}" , summary="Delect any product specific by product id",dependencies=[Depends(Auth)])
async def deleteProduct(id: int,token: str = Depends(oauth2_scheme)):
    try:
        session = Session()
        product = session.query(Product).get(id)
        session.delete(product)
        session.commit()
        return {"message": f"Product {product.name} has been deleted"}
    except Exception as ex:
        #return {"error": ex}
        return Response(status_code=status.HTTP_400_BAD_REQUEST),{"message": f"error: {ex}"}


if __name__ == '__main__':
    uvicorn.run(app=app, debug=True)
