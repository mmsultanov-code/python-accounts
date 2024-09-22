from fastapi import HTTPException, status, Depends, Response
from datetime import timedelta
from app.common.oauth2 import AuthJWT
from app.common.database import AsyncSession
from app.models.user import User as UserModel
from app.models.role import Role as RoleModel
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import logging as log
from config import Config

ACCESS_TOKEN_EXPIRES_IN = Config.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN  = Config.REFRESH_TOKEN_EXPIRES_IN

class AuthService:

    async def __get_user_by_email(session: AsyncSession, email: str) -> UserModel:
        try:
            user_stmt = select(UserModel).where(UserModel.email == email.lower())
            user = await session.execute(user_stmt)
            user = user.scalars().first()
            return user
        except Exception as e:
            log.error(e)
            raise Exception(e)

    async def __get_role_by_slug(session: AsyncSession, slug: str) -> RoleModel:
        try:
            role = await session.execute(select(RoleModel).where(RoleModel.slug == slug))
            role = role.scalars().first()

            if not role:
                log.error('Role not found')
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Role not found')

            return role
        except Exception as e:
            log.error(e)
            raise Exception(e)
    
    async def __hash_password(password: str) -> str:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
    
    async def __verify_password(password: str, hashed_password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(password, hashed_password)

    @staticmethod
    async def register_user(session: AsyncSession, payload):
        # Get user role
        role = await AuthService.__get_role_by_slug(session, "user_role")

        # Check if email already exists
        user = await AuthService.__get_user_by_email(session, payload.email.lower())
        if user:
            log.error('Email already exists')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')

        # hashing password
        payload.password = await AuthService.__hash_password(payload.password)
        del payload.passwordConfirm
        payload.role_id = role.id
        payload.email = payload.email.lower()

        # remove creator_id if it is 0
        if payload.creator_id == 0:
            payload.creator_id = None
        
        # Create new user
        new_user = UserModel(**payload.dict())
        session.add(new_user)
        
        # Commit transaction
        try:
            await session.commit()
            return {
                "status_code": status.HTTP_201_CREATED,
                "message": "User created successfully",
                "data": new_user
            }
        except Exception as e:
            log.error(e)
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    @staticmethod
    async def login(session: AsyncSession, payload, response: Response, Authorize: AuthJWT = Depends()):
        try:
            user = await AuthService.__get_user_by_email(session, payload.email.lower())
            verify_password = await AuthService.__verify_password(payload.password, user.password)
            if not verify_password:
                log.error('Invalid password')
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid password')

            # Create access token
            access_token = await Authorize.create_access_token(subject=str(user.id), expires_time=timedelta(minutes=int(Config.ACCESS_TOKEN_EXPIRES_IN)))

            # Create refresh token
            refresh_token = await Authorize.create_refresh_token(subject=str(user.id), expires_time=timedelta(minutes=int(Config.REFRESH_TOKEN_EXPIRES_IN)))

            # Store refresh and access tokens in cookie
            response.set_cookie('access_token', access_token, int(ACCESS_TOKEN_EXPIRES_IN) * 60, int(ACCESS_TOKEN_EXPIRES_IN) * 60, '/', None, False, True, 'lax')
            response.set_cookie('refresh_token', refresh_token, int(REFRESH_TOKEN_EXPIRES_IN) * 60, int(REFRESH_TOKEN_EXPIRES_IN) * 60, '/', None, False, True, 'lax')
            response.set_cookie('logged_in', 'True', int(ACCESS_TOKEN_EXPIRES_IN) * 60, int(ACCESS_TOKEN_EXPIRES_IN) * 60, '/', None, False, False, 'lax')

            my_permissions = await session.execute(select(RoleModel).filter(RoleModel.id == user.role_id).options(joinedload(RoleModel.permissions)))
            my_permissions = my_permissions.scalars().first().permissions
            my_permissions = [permission.slug for permission in my_permissions]
            
            return {
                "status_code": status.HTTP_200_OK,
                "message": "Login successful",
                "data": user
            }
        except Exception as e:
            log.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))