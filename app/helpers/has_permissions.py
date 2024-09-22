from functools import wraps
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.common.database import AsyncSession, engine
from app.models.user import User
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import joinedload
from app.models.role import Role

def has_permission(permissions: list):
    
    def decorator(func):
    
        @wraps(func)
    
        async def wrapper(*args, **kwargs):
            session = AsyncSession(bind=engine)
            user_id = kwargs.get('user_id')
            
            async with session.begin():
                try:
                    user = await session.execute(select(User).filter(User.id == int(user_id)))
                    user = user.scalars().first()
                    try:
                        role = await session.execute(select(Role).options(joinedload(Role.permissions)).filter(Role.id == user.role_id))
                        role = role.scalars().first()
                        user_permissions = [role['slug'] for role in jsonable_encoder(role.permissions)]
                    except Exception as e:
                        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
                except Exception as e:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
            
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
            
            existing_permissions = []

            for permission in permissions:
                if permission in user_permissions:
                    existing_permissions.append(permission)

            if not existing_permissions:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied")

            return await func(*args, **kwargs)
        
        return wrapper
    
    return decorator