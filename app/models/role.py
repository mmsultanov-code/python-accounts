from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.common.database import Base

class RolePermission(Base):
    __tablename__ = 'role_permission'
    role_id = Column(Integer, ForeignKey("role.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permission.id"), primary_key=True)

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    creator_id = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    
    permissions = relationship("Permission", secondary=RolePermission.__table__, back_populates="roles")

class Permission(Base):
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    roles = relationship("Role", secondary=RolePermission.__table__, back_populates="permissions")