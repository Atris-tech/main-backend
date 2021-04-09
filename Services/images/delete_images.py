from db_models.models.images_model import Image
from Services.type_sense.type_sense_crud_service import delete_collection
from Services.storage_services import delete_blob
from settings import TYPESENSE_IMAGES_INDEX


def delete_images(notes_obj, container_name):
    print(container_name)
    image_objs = Image.objects.filter(notes_id=notes_obj)
    for image_obj in image_objs:
        print(image_obj.blob_name)
        delete_collection(collections_id=str(image_obj.id), index=TYPESENSE_IMAGES_INDEX)
        delete_blob(container_name=container_name, blob_name=image_obj.blob_name)


def delete_single_image(image_obj, container_name):
    delete_collection(collections_id=str(image_obj.id), index=TYPESENSE_IMAGES_INDEX)
    delete_blob(container_name=container_name, blob_name=image_obj.blob_name)
    image_obj.delete()
