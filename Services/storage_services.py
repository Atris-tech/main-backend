from fastapi import HTTPException
from settings import AZURE_BLOB_STORAGE_CONNECTION_STRING, MAX_PROFILE_PHOTO_SIZE
from azure.storage.blob import BlobServiceClient, PublicAccess
from db_models.models.user_model import UserModel
import magic
import settings
from error_constants import INVALID_FILE_TYPE, FILE_SIZE_EXCEEDED
import uuid
from azure.core.exceptions import ResourceNotFoundError

blob_service_client = BlobServiceClient.from_connection_string(AZURE_BLOB_STORAGE_CONNECTION_STRING)


def get_or_create_container(email=False, notes_cont=False, user_model_obj=False):
    if not user_model_obj:
        user_model_obj = UserModel.objects.get(email_id=email)
    if notes_cont:
        container_name = user_model_obj.user_storage_notes_container_name
        if container_name is None:
            container_name = str(uuid.uuid1())
            user_model_obj.update(user_storage_notes_container_name=container_name)
        blob_service_client.create_container(name=container_name)
    else:
        container_name = user_model_obj.user_storage_container_name
        if container_name is None:
            container_name = str(uuid.uuid1())
            user_model_obj.update(user_storage_container_name=container_name)
        blob_service_client.create_container(name=container_name,
                                             public_access=PublicAccess.Container)
    return {"container_name": container_name, "user_model_obj": user_model_obj}


def upload_file_blob_storage(file_data, file_name, email=False, profile=False, save_note=False, bg=False,
                             container_name=False, user_model_obj=False):
    print("in upload blob storage")
    if profile:
        if len(file_data) > MAX_PROFILE_PHOTO_SIZE:
            raise HTTPException(
                status_code=FILE_SIZE_EXCEEDED["status_code"],
                detail=FILE_SIZE_EXCEEDED["detail"]
            )
    else:
        if not save_note:
            print("in else")
            file_extension = None
            mime_type = magic.from_buffer(buffer=file_data, mime=True)
            print(mime_type)
            if profile:
                to_check = settings.MIME_TYPES_IMAGES.items()
            else:
                to_check = settings.MIME_TYPES_AUDIO.items()
            for key, val in to_check:
                if str(mime_type) == val:
                    file_extension = key
                    break
            print(file_extension)
            if file_extension is None:
                print("file_extension none")
                if bg:
                    print("none bg")
                    """get file_data"""
                    return None
                else:
                    raise HTTPException(
                        status_code=INVALID_FILE_TYPE["status_code"],
                        detail=INVALID_FILE_TYPE["detail"]
                    )
        if not container_name:
            container_data = get_or_create_container(email=email, notes_cont=save_note, user_model_obj=user_model_obj)
            container_name = container_data["container_name"]
            user_model_obj = container_data["user_model_obj"]
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
        blob_client.upload_blob(file_data, overwrite=True)
        url = blob_client.url
        data = {"container_name": container_name, "url": url}
        print(data)
        print("blob uploaded")
        if profile:
            user_model_obj.update(image=url)
        return data


def delete_blob(container_name, blob_name):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    try:
        blob_client.delete_blob()
    except ResourceNotFoundError:
        print("file not found to delete")
