import uuid
from fastapi import HTTPException
from settings import AZURE_BLOB_STORAGE_CONNECTION_STRING, MAX_PROFILE_PHOTO_SIZE
from azure.storage.blob import BlobServiceClient, PublicAccess
from db_models.models.user_model import UserModel
import magic
import settings
from error_constants import INVALID_FILE_TYPE, FILE_SIZE_EXCEEDED


blob_service_client = BlobServiceClient.from_connection_string(AZURE_BLOB_STORAGE_CONNECTION_STRING)


def upload_profile(email, file_data, file_name):
    if len(file_data) > MAX_PROFILE_PHOTO_SIZE:
        raise HTTPException(
            status_code=FILE_SIZE_EXCEEDED["status_code"],
            detail=FILE_SIZE_EXCEEDED["detail"]
        )
    else:
        file_extension = None
        mime_type = magic.from_buffer(buffer=file_data, mime=True)
        for key, val in settings.MIME_TYPES_IMAGES.items():
            if str(mime_type) == val:
                file_extension = key
                break
        if file_extension is None:
            raise HTTPException(
                status_code=INVALID_FILE_TYPE["status_code"],
                detail=INVALID_FILE_TYPE["detail"]
            )
        user_model_obj = UserModel.objects.get(email_id=email)
        container_name = user_model_obj.user_storage_container_name
        if container_name is None:
            container_name = str(uuid.uuid1())
            container_client = blob_service_client.create_container(name=container_name,
                                                                    public_access=PublicAccess.Container)
            user_model_obj.update(user_storage_container_name=container_name)
        else:
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
            blob_client.upload_blob(file_data, overwrite=True)
            url = blob_client.url
            user_model_obj.update(image=url)
            return url
