from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import select
from app.common.database import get_async_session, AsyncSession
from app.common.oauth2 import AuthJWT
from app.common.exceptions.validation_exception import ValidationLoginException, ValidationRegisterException
from app.schemas.auth import GetUserAfterRegistrationSchema
from app.schemas.user import CreateUserSchema, UserLoginSchema, ResponseLoginUser
import logging as log
from app.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
)


@router.post('/register', response_model=GetUserAfterRegistrationSchema)
async def register(payload: CreateUserSchema, session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        try:
            ValidationRegisterException(payload)
            auth_service = AuthService()
            user = await auth_service.register_user(session, payload)
            return user
        except Exception as e:
            log.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
@router.post('/login', response_model=ResponseLoginUser)
async def login(payload: UserLoginSchema, response: Response, session: AsyncSession = Depends(get_async_session), Authorize: AuthJWT = Depends()):
    async with session.begin():
        try:
            ValidationLoginException(payload)
            auth_service = AuthService()
            auth = await auth_service.login(session, payload, response, Authorize)
            return auth
        except Exception as e:
            log.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))