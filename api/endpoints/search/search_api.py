from fastapi import APIRouter, Request, HTTPException, Query
import error_constants
from Services.auth.auth_services import token_check
from search.search_test import search_notes, search_images, search_audio, filter_tag

router = APIRouter()


@router.get("/note_search/", status_code=200)
def note_search(
        request: Request,
        note_name: str = Query(None, max_length=20),

):
    if note_name is not None:
        user_dict = token_check(request)
        return search_notes(
            email=user_dict["email_id"],
            query=note_name
        )
    else:
        raise HTTPException(
            status_code=error_constants.NoneValue.code,
            detail=error_constants.NoneValue.detail
        )


@router.get("/image_search/", status_code=200)
def image_search(
        request: Request,
        image: str = Query(None, max_length=20),

):
    if image is not None:
        user_dict = token_check(request)
        return search_images(
            email=user_dict["email_id"],
            query=image
        )
    else:
        raise HTTPException(
            status_code=error_constants.NoneValue.code,
            detail=error_constants.NoneValue.detail
        )


@router.get("/audio_search/", status_code=200)
def audio_search(
        request: Request,
        audio: str = Query(None, max_length=20),
):
    if audio is not None:
        user_dict = token_check(request)
        return search_audio(
            email=user_dict["email_id"],
            query=audio
        )
    else:
        raise HTTPException(
            status_code=error_constants.NoneValue.code,
            detail=error_constants.NoneValue.detail
        )


@router.get("/filter_tags/", status_code=200)
def filter_tags(
        request: Request,
        tag_name: str = Query(None, max_length=20),

):
    if tag_name is not None:
        user_dict = token_check(request)
        return filter_tag(
            email=user_dict["email_id"],
            tag_id=tag_name
        )
    else:
        raise HTTPException(
            status_code=error_constants.NoneValue.code,
            detail=error_constants.NoneValue.detail
        )
