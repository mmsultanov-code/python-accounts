from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv('DB_PASS')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    ORIGIN = os.getenv('ORIGIN')
    
    ACCESS_TOKEN_EXPIRES_IN = os.getenv('ACCESS_TOKEN_EXPIRES_IN')
    REFRESH_TOKEN_EXPIRES_IN = os.getenv('REFRESH_TOKEN_EXPIRES_IN')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
    CLIENT_ORIGIN = os.getenv('CLIENT_ORIGIN')
    PRIVATE_KEY = os.getenv('PRIVATE_KEY')
    PUBLIC_KEY = os.getenv('PUBLIC_KEY')
    REDIS_URL = os.getenv('REDIS_URL')
    REDIS_TIMEOUT = os.getenv('REDIS_TIMEOUT')

    JWT_PRIVATE_KEY = os.getenv('JWT_PRIVATE_KEY')
    JWT_PUBLIC_KEY = os.getenv('JWT_PUBLIC_KEY')
    ACCESS_TOKEN_EXPIRES_IN = os.getenv('ACCESS_TOKEN_EXPIRES_IN')
    REFRESH_TOKEN_EXPIRES_IN = os.getenv('REFRESH_TOKEN_EXPIRES_IN')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')