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
    """
    Register a new user.

    Parameters:
    - payload: `CreateUserSchema` - The payload containing user registration data.
    - session: `AsyncSession` (optional) - The database session to use for the operation.

    Returns:
    - User - The newly registered user.

    Raises:
    - HTTPException - If an error occurs during the registration process.

    """
    async with session.begin():
        try:
            ValidationRegisterException(payload)
            user = await AuthService.register_user(session, payload)
            return user
        except Exception as e:
            log.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
@router.post('/login', response_model=ResponseLoginUser)
async def login(payload: UserLoginSchema, response: Response, session: AsyncSession = Depends(get_async_session), Authorize: AuthJWT = Depends()):
    """
    Login function for authenticating a user.

    Parameters:
    - payload (UserLoginSchema): The user login payload containing the username and password.
    - response (Response): The response object to send back to the client.
    - session (AsyncSession, optional): The async session to use for database operations. Defaults to the session obtained from `get_async_session` dependency.
    - Authorize (AuthJWT, optional): The AuthJWT instance for handling JWT authentication. Defaults to the instance obtained from `Depends()`.

    Returns:
    - auth: The authentication result.

    Raises:
    - HTTPException: If there is an internal server error during the login process.
    """
    async with session.begin():
        try:
            ValidationLoginException(payload)
            auth = await AuthService.login(session, payload, response, Authorize)
            return auth
        except Exception as e:
            log.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))