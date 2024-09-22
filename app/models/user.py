from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, validates

from app.common.database import Base

class User(Base):
    
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    role = relationship('Role')
    creator_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    updated_by = Column(Integer, ForeignKey('user.id'), nullable=True)
    creator = relationship('User', remote_side=[id], foreign_keys=[creator_id])
    updater = relationship('User', remote_side=[id], foreign_keys=[updated_by])

    @validates('email')
    def validate_email(self, key, email):
        assert len(email) > 10
        assert '@' in email
        return email
    
    @validates('password')
    def validate_password(self, key, password):
        assert len(password) > 4
        return password