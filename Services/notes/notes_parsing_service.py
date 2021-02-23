from db_models.models.notes_model import NotesModel
from db_models.models.workspace_model import WorkSpaceModel
from fastapi import HTTPException
import error_constants
from error_constants import BAD_REQUEST
from mongoengine.queryset.visitor import Q
from db_models.models.user_model import UserModel
import html2text
import re
import uuid

text_maker = html2text.HTML2Text()
text_maker.ignore_links = True
text_maker.bypass_tables = False
text_maker.UNICODE_SNOB = True
text_maker.ESCAPE_SNOB = True
text_maker.IGNORE_IMAGES = True


def check_notes(name):
    try:
        NotesModel.objects.get(notes_name=name)
        return True
    except NotesModel.DoesNotExist:
        return False


def check_user_workspace(workspace_name, email, user_obj):
    try:
        user_obj = UserModel.objects.get(email_id=email)
        WorkSpaceModel.objects(Q(user_id=user_obj) & Q(work_space_name=workspace_name))
        return True
    except UserModel.DoesNotExist:
        raise HTTPException(
            status_code=error_constants.INVALID_EMAIL["status_code"],
            detail=error_constants.INVALID_EMAIL["detail"]
        )


def html_to_text(data):
    text = text_maker.handle(data)
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('\\n', ' ').replace('\\', ' ')
    text = re.sub(' +', ' ', text)
    return text

def new_notes(workspace_name, email, data):
    check_user_workspace(workspace_name, email, user_obj)
    if check_notes(name):
        raise HTTPException(
            status_code=200,
            detail="notes exists"
        )
    else:
        user_object_model = UserModel.objects.get(email_id=email)
        text = html_to_text(data)
        notes_model_obj = NotesModel()
        notes_model_obj.user_id = user_object_model
        notes_model_obj.notes_name = name
        notes_model_obj.clean_text = text
        notes_model_obj.save()



def rename_workspace(old_notes_name, new_notes_name=False):
    try:
        notes_model_object = NotesModel.objects.get(notes_name=old_notes_name)
        if new_notes_name:
            notes_model_object.update(notes_name=new_notes_name)
        return True
    except NotesModel.DoesNotExist:
        raise HTTPException(
            status_code=BAD_REQUEST["status_code"],
            detail=BAD_REQUEST["detail"]
        )


def delete_workspace(notes_name):
    try:
        notes_model_obj = NotesModel.objects.get(notes_name=notes_name)
        notes_model_obj.delete()
        return True
    except NotesModel.DoesNotExist:
        raise HTTPException(
            status_code=BAD_REQUEST["status_code"],
            detail=BAD_REQUEST["detail"]
        )
