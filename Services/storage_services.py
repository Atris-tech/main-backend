from datetime import datetime, timedelta
from fastapi import HTTPException
from settings import MAX_PROFILE_PHOTO_SIZE, AZURE_STORAGE_KEY, AZURE_BLOB_STORAGE_NAME, AZURE_BLOB_STORAGE_URL
from db_models.models.user_model import UserModel
from error_constants import FILE_SIZE_EXCEEDED
import uuid
from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions, \
    PublicAccess

sas_token = generate_account_sas(
    account_name=AZURE_BLOB_STORAGE_NAME,
    account_key=AZURE_STORAGE_KEY,
    resource_types=ResourceTypes(service=True, container=True, object=True),
    permission=AccountSasPermissions(read=True, write=True, update=True, delete=True, list=True, add=True, create=True),
    expiry=datetime.utcnow() + timedelta(days=2)
)

blob_service_client = BlobServiceClient(account_url=AZURE_BLOB_STORAGE_URL, credential=sas_token)


def get_or_create_container(email=False, notes_cont=False, user_model_obj=False):
    if not user_model_obj:
        print("in not user model obj")
        user_model_obj = UserModel.objects.get(email_id=email)
    print(user_model_obj)
    if notes_cont:
        container_name = user_model_obj.user_storage_notes_container_name
        if container_name is None:
            container_name = str(uuid.uuid1())
            user_model_obj.update(user_storage_notes_container_name=container_name)
            blob_service_client.create_container(name=container_name, )
    else:
        container_name = user_model_obj.user_storage_container_name
        print("container name")
        print(container_name)
        if container_name is None:
            container_name = str(uuid.uuid1())
            user_model_obj.update(user_storage_container_name=container_name)
            blob_service_client.create_container(name=container_name,
                                                 public_access=PublicAccess.Container)
    return {"container_name": container_name, "user_model_obj": user_model_obj}


def upload_file_blob_storage(file_data, file_name, email=False, profile=False, save_note=False,
                             container_name=False, user_model_obj=False):
    print("in upload blob storage")
    if profile:
        if len(file_data) > MAX_PROFILE_PHOTO_SIZE:
            raise HTTPException(
                status_code=FILE_SIZE_EXCEEDED["status_code"],
                detail=FILE_SIZE_EXCEEDED["detail"]
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
