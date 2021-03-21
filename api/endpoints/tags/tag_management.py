from fastapi import APIRouter, Request, HTTPException
import error_constants
from Services.auth.auth_services import token_check
from Services.tags_services import create_new_tag, remove_tag, recommend_tag
from api.endpoints.tags.models import TagsApiModel, TagsDeleteModel

router = APIRouter()


@router.post("/add_tags/", status_code=200)
def create_new_tag_method(
        add_tags_obj: TagsApiModel,
        request: Request,

):
    user_dict = token_check(request)
    return create_new_tag(email=user_dict["email_id"], tag_name=add_tags_obj.tag_name, notes_id=add_tags_obj.notes_id,
                          workspace_id=add_tags_obj.workspace_id)


@router.post("/delete_tags/", status_code=200)
def remove_tag_method(
        tag_delete_obj: TagsDeleteModel,
        request: Request,

):
    user_dict = token_check(request)
    return remove_tag(
        tag_id=tag_delete_obj.tag_id,
        notes_id=tag_delete_obj.notes_id,
        email=user_dict["email_id"]
    )


@router.get("/get_matching_tags/", status_code=200)
def remove_tag_method(
        tag_name: str,
        request: Request,

):
    max_length = 15
    if len(tag_name) > max_length:
        raise HTTPException(
            status_code=error_constants.MaxTagsNameExceeded.code,
            detail=error_constants.MaxTagsNameExceeded.detail
        )
    user_dict = token_check(request)
    return recommend_tag(
        tag_query_name=tag_name,
        email=user_dict["email_id"]
    )
