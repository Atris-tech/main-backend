from Services.audios.audio_upload_helper import audio_save_to_db
from fastapi import Request, APIRouter, HTTPException
from pydantic import BaseModel
from jose import JWTError, jwt


from settings import TYPESENSE_AUDIO_INDEX
from Services.type_sense.type_sense_crud_service import create_collection
from Services.type_sense.typesense_dic_generator import generate_typsns_data

router = APIRouter()

def verify_token(request):
    token = request.headers.get("Authorization")
    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Authorization Error"
        )
    token = token.split()
    token = token[1]
    try:
        jwt.decode(token, "09d25e094fdf6ca25d6c81f166b7a9563g93f7099h6f0f4caa6cfj3b88e8d3e7",
                   algorithms=["HS256"])
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail="Authorization Error"
        )


class SaveToDbHook(BaseModel):
    blob_size: str
    stt_data: dict
    note_id: str
    file_url: str
    file_name: str
    original_file_name: str
    y_axis: str
    user_id: str


@router.post("/save_to_db_hook/", status_code=200)
def save_to_db_hook_call(
        request: Request,
        save_to_db_hook: SaveToDbHook
):
    pass
    verify_token(request)
    audio_obj_dict = audio_save_to_db(file_size=save_to_db_hook.blob_size, stt_data=save_to_db_hook.stt_data,
                                      notes_id=save_to_db_hook.note_id,
                                      url=save_to_db_hook.file_url, blob_name=save_to_db_hook.file_name,
                                      name=save_to_db_hook.original_file_name, y_axis=save_to_db_hook.y_axis)
    if audio_obj_dict is not None:
        if "transcribe" not in save_to_db_hook.stt_data:
            stt_data["transcribe"] = ""
        if "sound_recog_results" not in save_to_db_hook.stt_data:
            stt_data["sound_recog_results"] = []
        tps_dic = generate_typsns_data(obj=audio_obj_dict["audio_results_obj"], audio_data=save_to_db_hook.stt_data,
                                       audio_id=str(audio_obj_dict["audio_obj"].id),
                                       audio_name=audio_obj_dict["audio_obj"].name)
        create_collection(index=TYPESENSE_AUDIO_INDEX, data=tps_dic)
        return {
                "data": {
                    "status": "PROCESSED",
                    "task": "Audio Processing",
                    "audio_id": str(audio_obj_dict["audio_obj"].id),
                    "note_name": audio_obj_dict["note_name"],
                }
            }
    else:
        return "false"
