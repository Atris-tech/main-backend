from fastapi import APIRouter

from . import upload_api, generate_entity_emotion, generate_summary_kwrds, audio_management, image_management, \
    scrible_management


def routing():
    router = APIRouter()
    """include child api routes"""
    router.include_router(upload_api.router)
    router.include_router(generate_summary_kwrds.router)
    router.include_router(generate_entity_emotion.router)
    router.include_router(audio_management.router)
    router.include_router(image_management.router)
    router.include_router(scrible_management.router)
    return router
