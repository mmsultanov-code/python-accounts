import base64
from datetime import timedelta
from typing import List
from fastapi import Depends, HTTPException, status
from async_fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from sqlalchemy import select
from app.common.database import AsyncSession, get_async_session
from app.models.user import User as UserModel

from config import Config
JWT_ALGORITHM = Config.JWT_ALGORITHM
PUBLIC_KEY = Config.JWT_PUBLIC_KEY
PRIVATE_KEY = Config.JWT_PRIVATE_KEY

class Settings(BaseModel):
    authjwt_algorithm: str = JWT_ALGORITHM
    authjwt_decode_algorithms: List[str] = [JWT_ALGORITHM]
    authjwt_token_location: set = {'cookies'}
    authjwt_cookie_csrf_protect: bool = False
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_public_key: str = base64.b64decode(PUBLIC_KEY).decode('utf-8')
    authjwt_private_key: str = base64.b64decode(PRIVATE_KEY).decode('utf-8')
    authjwt_access_token_expires: timedelta = timedelta(minutes=30)
    authjwt_refresh_token_expires: timedelta = timedelta(days=30)
    authjwt_access_csrf_cookie_key: str = "access_token_csrf"
    authjwt_refresh_csrf_cookie_key: str = "refresh_token_csrf"



@AuthJWT.load_config
def get_config():
    return Settings()

class NotVerified(Exception):
    pass


class UserNotFound(Exception):
    pass

async def require_user(session: AsyncSession = Depends(get_async_session), Authorize: AuthJWT = Depends()):
    async with session.begin():
        try:
            await Authorize.jwt_required()
            user_id = await Authorize.get_jwt_subject()
            user = await session.execute(select(UserModel).where(UserModel.id == int(user_id)))
            user = user.scalars().first()

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User no longer exist")

        except Exception as e:
            await session.rollback()
            error = e.__class__.__name__

            if error == 'MissingTokenError':
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in")
            
            if error == 'UserNotFound':
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User no longer exist")
            
            if error == 'NotVerified':
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please verify your account")
            
            if error == 'AttributeError':
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Something attribute error")
            
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid or has expired")
        
        return user_id