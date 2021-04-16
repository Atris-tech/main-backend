import mimetypes
import os
import shutil

from fastapi import Request, APIRouter, HTTPException, Cookie, Query, BackgroundTasks
from fastapi.responses import StreamingResponse
from mongoengine import Q

from Services.audios.delete_audio_service import delete_single_storage_object
from Services.auth.auth_services import token_check
from Services.storage_services import StorageServices
from Services.type_sense.type_sense_crud_service import delete_collection
from api.endpoints.notes.models import ImageDeleteModel
from db_models.models.images_model import Image
from db_models.models.user_model import UserModel
from db_models.models.tags_model import TagModel
from error_constants import BadRequest, NotFound
from settings import TYPESENSE_IMAGES_INDEX, MAX_NOTES_ID, MIN_NOTES_ID

router = APIRouter()


def delete_image_folder(folder_name):
    print("deleting folder")
    shutil.rmtree(folder_name)


@router.get("/get_image/", status_code=200)
def read_items(background_tasks: BackgroundTasks, request: Request, img_id: str = Query(None, min_length=MAX_NOTES_ID,
                                                                                        max_length=MIN_NOTES_ID),
               token: str = Cookie(None)):
    if token is not None:
        user_dict = token_check(request, direct_token=token, refresh_token=True, rf_dict=True)
        print(user_dict)
        print("user_dict")
        user_obj = UserModel.objects.get(email_id=user_dict["email_id"])
        try:
            image_obj = Image.objects.get(id=img_id)
            download_obj = StorageServices().download_blob(container_name=user_obj.user_storage_container_name,
                                                           blob_id=image_obj.blob_name, obj=True)
            if download_obj:
                new_folder = os.path.join("Uploads", str(user_obj.id))
                try:
                    os.mkdir(new_folder)
                except FileExistsError:
                    print("directory exists")
                image_file = os.path.join(new_folder, str(image_obj.blob_name))
                with open(image_file, "wb") as download_file:
                    download_file.write(download_obj.readall())
                file_obj = open(image_file, "rb")
                background_tasks.add_task(delete_image_folder, folder_name=new_folder)
                return StreamingResponse(file_obj, media_type=mimetypes.guess_type(image_file)[0])
            else:
                raise HTTPException(
                    status_code=NotFound.code,
                    detail=NotFound.detail
                )
        except Image.DoesNotExist:
            raise HTTPException(
                status_code=NotFound.code,
                detail=NotFound.detail
            )
    else:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )


@router.post("/delete_image/", status_code=200)
def delete_image(
        request: Request,
        image_delete_obj: ImageDeleteModel,
):
    user_dict = token_check(request)
    try:
        user_obj = UserModel.objects.get(email_id=user_dict["email_id"])
        image_obj = Image.objects.get(Q(user_id=user_obj) & Q(id=image_delete_obj.image_id))
        delete_collection(collections_id=str(image_obj.id), index=TYPESENSE_IMAGES_INDEX)
        delete_single_storage_object(obj=image_obj, container_name=user_obj.user_storage_container_name)
        return True
    except Image.DoesNotExist:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail + " or note deleted before"
        )
