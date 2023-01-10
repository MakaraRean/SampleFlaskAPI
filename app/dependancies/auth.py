from fastapi import Depends, Request, HTTPException
from fastapi.openapi.models import Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from starlette import status

from app.models.models import User
from database import Session

security = HTTPBearer()

SECTET_KEY = "2DF97463AF0944F4F459BC06E5CF8D47"  # is secret key to extend with user password when add to database, when compare you need to cut it out first
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 30





async def authentication(request: Request,authorize_credential: HTTPAuthorizationCredentials = Depends(security)):

    access_token = authorize_credential.credentials
    if authorize_credential.scheme != "Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid authentication scheme.")
    try:
        access_token_payload = jwt.decode(access_token,key=SECTET_KEY,algorithms=ALGORITHM)
        username = access_token_payload.get('sub')
        session = Session()
        user = session.query(User).filter_by(username=username).first()
        if user:
            request.state.user_id = user.id
            request.state.username = user.username
            # context.data["x-user-info"] = request.headers.get('x-user-info') or ''
            # context.data["x-user"] = user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Signature expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid authentication token")
    return user