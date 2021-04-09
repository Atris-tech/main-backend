from Services.auth.auth_services import token_check
from search.search_test import search_audio, search_notes, search_images
from fastapi import Request, File, UploadFile, HTTPException, Header, Depends, BackgroundTasks, Form, APIRouter
from error_constants import NotFound
from db_models.models.user_model import UserModel

router = APIRouter()


@router.post("/note_search/", status_code=200)
def note_search(
        request: Request,
        note: str = Form(...),
):
    user_dict = token_check(request)
    user_obj = UserModel.objects.get(email_id=user_dict["email_id"])



@router.post("/audio_search/", status_code=200)
def note_search():
    pass


@router.post("/image_search/", status_code=200)
def note_search():
    pass