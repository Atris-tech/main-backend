from fastapi import APIRouter
from .import upload_api


def routing():
    router = APIRouter()
    """include child api routes"""
    router.include_router(upload_api.router)
    return router

