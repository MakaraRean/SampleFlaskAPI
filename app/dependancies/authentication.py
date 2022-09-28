import base64
import datetime
import logging
from datetime import timedelta
from typing import Union, Optional
import bcrypt
from fastapi import Depends, FastAPI, HTTPException, Response, Request, Header,Security
from fastapi.security import OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer, HTTPBearer
from flask import jsonify
from pydantic import BaseModel
from starlette.responses import JSONResponse
from app.dependancies.auth import authentication as Auth, SECTET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

#from app.security.oauth2 import  OAuth2PasswordRequestForm,OAuth2AuthorizationCodeBearer
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette import status

from app.models.models import User
from database import Session
from routes.routers import user
from app.pydantic.request import User as requestUser, TokenData, RefreshToken
from passlib.context import CryptContext
from jose import jwt

router = FastAPI()
app = user
oauth2_scheme = HTTPBearer()


class Settings(BaseModel):
    authjwt_secret_key = SECTET_KEY
    authjwt_denylist_enabled: bool = True
    auth_denylist_token_checks: set = {"access": "refresh"}
    access_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires = timedelta(days=30)


class Token(BaseModel):
    access_token: Optional[str] = None,
    refresh_token: str


@AuthJWT.load_config
def get_config():
    return Settings()


@router.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exception: AuthJWTException):
    return JSONResponse(
        status_code=status,
        content={"detail": exception.message}
    )

denylist = set()
@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token["jti"]
    return jti in denylist


def create_access_token(data: dict, expired: Union[timedelta, None] = None):
    # to_encode = data.copy()
    if expired:
        expire = datetime.datetime.utcnow() + expired
    else:
        expire = datetime.datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": data}
    # to_encode = data.update({"exp": expire,"sub": data})
    encode_jwt = jwt.encode(to_encode, key=SECTET_KEY, algorithm=ALGORITHM)
    return encode_jwt


# def create_refresh_token():

# async def refresh_token(token: str = Depends(oauth2_scheme)):
#     payload = jwt.decode(token, SECTET_KEY, algorithms=[ALGORITHM])
#     sub = payload.get("sub")
#     exp = payload.get("exp")
#     if exp:
#         expire = datetime.datetime.utcnow() + exp
#     else:
#         expire = datetime.datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode = {"exp": expire, "sub": sub}
#     # refresh_token = create_access_token(data=sub,expired=exp)
#     token_refresh = jwt.encode(to_encode, key=SECTET_KEY, algorithm=ALGORITHM, access_token=token)
#     print("Hello World")
#     return Response({"refresh_token": token_refresh, "old_token": token}, status_code=status.HTTP_200_OK)


def sample_decode_token(token):
    return User(username=token, password=123)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return user_dict

async def get_current_user(response: Response,authorize: HTTPBearer = Depends(oauth2_scheme)):
    return authorize
# async def get_current_user(token: str = Depends(oauth2_scheme)): user with jose
#     credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                          detail="Could not validate credential", headers={"WWW-Authenticate": "Bearer"})
#     try:
#         payload = jwt.decode(token, SECTET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         exp = payload.get("exp")
#         session = Session()
#         userDB = session.query(User).filter_by(username=username).first()
#         if username is None:
#             raise credentials_exeption
#     except JWTError:
#         raise credentials_exeption
#     return {"id": userDB.id, "username": username, "exp": exp, "token": token}


@app.get("/user/me", summary="Get auth user", dependencies=[Depends(Auth)])
async def authUser(current_user: User = Depends(get_current_user),token: HTTPBearer = Depends(oauth2_scheme)):
    # payload = jwt.decode(token=token,key=SECTET_KEY,algorithms=ALGORITHM)
    # credential = payload.get('credentials')
    # print(credential)
    # try:
    #     print(token.get_raw_jwt()['token']+"ok")
    #     if token.get_raw_jwt()['sub']:
    #         return current_user
    # except Exception as ex:
    #     return {"message": "Token invalid", "Exeption": ex}
    print(token.credentials)
    try:
        if token.credentials == Token.access_token:
            return current_user
    except HTTPException as ex:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=ex.detail)




@app.get("/getHeader", summary="Get header information", dependencies=[Depends(Auth)])
async def getHeader(request: Request, authorize: str = Depends(oauth2_scheme)):
    return {"header": request.headers,"auth": authorize}


@app.post("/register", summary="Create new user")
async def register(request: requestUser):
    try:
        session = Session()
        user = User(
            username=request.username,
            password=CryptContext(schemes=['bcrypt'], deprecated="auto").hash(request.password) + SECTET_KEY
        )
        session.add(user)
        session.commit()
        return {"message": "New user create successfully"}
    except Exception as ex:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username is already exist.")


def verify_password(password: str, hashed_password: str) -> bool:
    if isinstance(password, str):  # endcode passsword before checking
        password = password.encode()
    verified_hash = hashed_password.replace(SECTET_KEY, "")
    # check_hash = CryptContext(schemes=['bcrypt'], deprecated="auto").hash(password)
    return bcrypt.checkpw(password, verified_hash.encode())


@app.post("/token", summary="Login and response token")
async def login(request: requestUser, authorize: AuthJWT = Depends()): #form_data: OAuth2PasswordRequestForm = Depends() use form_data form request data from endpoint using form
    session = Session()
    users = session.query(User).filter_by(username=request.username).first()
    if users:  # check if username is valid

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "exp": access_token_expires,
            "iat": datetime.datetime.now(),
            "sub": users.id,
            "username": users.username
        }

        #access_token = jwt.encode(payload,key=SECTET_KEY,algorithm=ALGORITHM)
        access_token = authorize.create_access_token(subject=users.username, expires_time=access_token_expires,
                                                      algorithm=ALGORITHM,fresh=True)
        refresh_token = authorize.create_refresh_token(subject=users.username,expires_time=timedelta(days=30))

        # access_token = AuthJWT._create_token(self=users.username,algorithm=ALGORITHM,type_token="Bearer",subject=users.username,exp_time= int(str(access_token_expires)))

        checkPass = verify_password(request.password, users.password)
        if checkPass:  # if password is matched
            if users.username == request.username:
                Token.access_token = access_token
                Token.refresh_token = refresh_token
                print({"access_token": Token.access_token,"\nrefresh_token": refresh_token})
                Header({"Content-type": "application/json",
                          "Accept": "application/json",
                          "Authorization": f"Bearer {refresh_token}"})
                return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
        elif not checkPass and users.username == request.username:  # if password is incorrect but username is correct
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is incorrect",
                                 headers={"WWW-Authenticate": "Bearer"})
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username is incorrect",
                             headers={"WWW-Authenticate": "Bearer"})


@app.post("/refresh_token",name="refresh_token")
def refresh_token(request: RefreshToken,authorize: AuthJWT = Depends()):
    payload = jwt.decode(request.refresh,key=SECTET_KEY,algorithms=ALGORITHM)
    sub = payload.get('sub')
    print(sub)
    new_access_token = authorize.create_access_token(subject= sub,expires_time=ACCESS_TOKEN_EXPIRE_MINUTES,algorithm=ALGORITHM,fresh=True)
    Token.access_token = new_access_token
    return {"access_token": new_access_token}

# @app.delete("/access_revoke")
# def access_revoke(authorize: AuthJWT = Depends()):
#     authorize.jwt_required()
#
#     jti = authorize.get_raw_jwt()["jti"]
#     denylist.add(jti)
#     return {"detail": "Aceess token has been revoke"}
#
# @app.delete("/refresh_revoke")
# def refresh_revoke(authorize: AuthJWT = Depends()):
#     authorize.jwt_refresh_token_required()
#
#     jti = authorize.get_raw_jwt()["jti"]
#     denylist.add(jti)
#     return {"detail": "Refresh token has been revoke"}
#
#
# @app.get("/protected")
# def protected(authorize: AuthJWT = Depends()):
#     authorize.jwt_required()

    # auth_user = authorize.get_jwt_subject()
    # return {"user": auth_user}