from setuptools import setup, find_packages

setup(
    name='auth_api_server',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'fastapi[all]',
        'passlib[bcrypt]',
        'alembic',
        'sqlalchemy',
        'async-fastapi-jwt-auth[asymmetric]',
        'httpx',
        'asyncio',
        'asyncpg',
        'psycopg2',
        'fastapi-cache2[redis]'
    ],
)
# pip install -e .