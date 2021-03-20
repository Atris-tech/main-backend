from fastapi import APIRouter, Request, HTTPException
from pydantic import AnyStrMinLengthError, AnyStrMaxLengthError, BaseModel, validator

import error_constants
from Services.auth.auth_services import token_check
from Services.tags_services import create_new_tag, remove_tag, recommend_tag


router = APIRouter()


class TagsApiModel(BaseModel):
    tag_name: str
    workspace_id: str
    notes_id: str

    @validator('tag_name')
    def has_max_length(cls, v):
        max_length = 15
        if len(v) > max_length:
            raise AnyStrMaxLengthError(limit_value=max_length)
        return v

    @validator('workspace_id', 'notes_id')
    def has_min_length(cls, v):
        min_length = 24
        if len(v) < min_length:
            raise AnyStrMinLengthError(limit_value=min_length)
        return v


@router.post("/add_tags/", status_code=200)
def create_new_tag_method(
        add_tags_obj: TagsApiModel,
        request: Request,

):
    user_dict = token_check(request)
    return create_new_tag(email=user_dict["email_id"], tag_name=add_tags_obj.tag_name, notes_id=add_tags_obj.notes_id,
                          workspace_id=add_tags_obj.workspace_id)


class TagsDeleteModel(BaseModel):
    tag_id: str
    notes_id: str

    class Config:
        min_anystr_length = 24
        error_msg_templates = {
            'value_error.any_str.min_length': 'min_length:{limit_value}',
        }


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
            status_code=error_constants.MAX_TAGS_NAME_EXCEEDED["status_code"],
            detail=error_constants.MAX_TAGS_NAME_EXCEEDED["detail"]
        )
    user_dict = token_check(request)
    return recommend_tag(
        tag_query_name=tag_name,
        email=user_dict["email_id"]
    )
