from fastapi import APIRouter, Request, HTTPException, Query

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
    tags_ids = list()
    for tag_name in add_tags_obj.tags_name:
        tag_id = create_new_tag(email=user_dict["email_id"], tag_name=tag_name, notes_id=add_tags_obj.notes_id,
                                workspace_id=add_tags_obj.workspace_id)
        tags_ids.append(tag_id)
    return tags_ids


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
        request: Request,
        tag_name: str = Query(None, max_length=15),

):
    if tag_name is None:
        raise HTTPException(
            status_code=error_constants.NoneValue.code,
            detail=error_constants.NoneValue.detail
        )
    user_dict = token_check(request)
    return recommend_tag(
        tag_query_name=tag_name,
        email=user_dict["email_id"]
    )
