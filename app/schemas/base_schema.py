from enum import Enum
from pydantic import BaseModel, EmailStr

class LanguageEnum(str, Enum):
    ru = "ru"
    uz = "uz"
    en = "en"

class StatusEnumStr(str, Enum):
    public = 'public'
    private = 'private'
    draft = 'draft'
    archive = 'archive'

class ProductTypeEnum(str, Enum):
    tariffs = 'tariffs'
    services = 'services'
    packages = 'packages'

class PerdiodEnum(str, Enum):
    P1D = "P1D"
    P3D = "P3D"
    P7D = "P7D"
    P14D = "P14D"
    P15D = "P15D"
    P30D = "P30D"
    P31D = "P31D"
    P1M = "P1M"
    P1Y = "P1Y"
    
class UserInListSchema(BaseModel):
    name: str
    email: EmailStr
    avatar: str

    class Config:
        orm_mode = True
        exclude = {'id', 'password', 'role_id'}

class ELementorDataList(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        orm_mode = True