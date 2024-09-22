from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
app = FastAPI(
    title="Auth Service",
    description="Auth Service API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[Config.CLIENT_ORIGIN, 'http://localhost:3000'],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=500)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


from app.controller.auth import router as auth_router
from app.controller.account import router as account_router

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(account_router, prefix="/account", tags=["account"])