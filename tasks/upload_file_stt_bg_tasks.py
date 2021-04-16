import uuid

from Services.api_call_service import api_call
from Services.audios.audio_upload_helper import audio_save_to_db
from Services.redis_service import get_list, get_val, redis_publisher_serv
from Services.storage_services import StorageServices
from Services.type_sense.type_sense_crud_service import create_collection
from Services.type_sense.typesense_dic_generator import generate_typsns_data
from settings import TYPESENSE_AUDIO_INDEX
from task_worker_config.celery import app


def upload_task(user_obj, file_data, file_name, notes_id, blob_size, audio_request_id, original_file_name, y_axis,
                workspace_id, note_name):
    file_name = str(uuid.uuid4()) + file_name
    print(blob_size)
    data = StorageServices().upload_file_blob_storage(file_data=file_data, file_name=file_name, user_model_obj=user_obj)
    print("data")
    print(data)
    if data:
        print("in data")
        url = data["url"]
        direct_api_supported_plans = get_list("DIRECT_STT_API_PLANS")
        if user_obj.plan in direct_api_supported_plans:
            print("background_tasks")
            stt_end_point = get_val(key="STT_UPLOAD_URL")
            f_align_end_point = get_val(key="FORCED_ALIGN_UPLOAD_URL")
            sound_recog_endpoint = get_val(key="SOUND_RECOG_ENDPOINT")
            stt_data = api_call(file_to_process=file_data, end_point=stt_end_point,
                                f_align_end_point=f_align_end_point, sound_recog_endpoint=sound_recog_endpoint,
                                binary=True, file_name=file_name)
            print("stt_data")
            print(stt_data)
            if stt_data:
                audio_obj_dict = audio_save_to_db(file_size=blob_size, stt_data=stt_data, notes_id=notes_id,
                                                  url=url, blob_name=file_name, name=original_file_name, y_axis=y_axis)
                if audio_obj_dict is not None:
                    if "transcribe" not in stt_data or stt_data["transcribe"] is None:
                        stt_data["transcribe"] = ""
                    if "sound_recog_results" not in stt_data or stt_data["sound_recog_results"]:
                        stt_data["sound_recog_results"] = []
                    to_send_ws_data = {
                        "client_id": str(user_obj.id),
                        "data": {
                            "status": "PROCESSED",
                            "task": "Audio Processing",
                            "audio_request_id": audio_request_id,
                            "audio_id": str(audio_obj_dict["audio_obj"].id),
                            "note_id": notes_id,
                            "note_name": audio_obj_dict["note_name"],
                            "workspace_id": workspace_id
                        }
                    }
                    print(to_send_ws_data)
                    tps_dic = generate_typsns_data(obj=audio_obj_dict["audio_results_obj"], audio_data=stt_data,
                                                   audio_id=str(audio_obj_dict["audio_obj"].id),
                                                   audio_name=audio_obj_dict["audio_obj"].name)
                    print(tps_dic)
                    create_collection(index=TYPESENSE_AUDIO_INDEX, data=tps_dic)
                    redis_publisher_serv(channel=str(user_obj.id), data=to_send_ws_data)
                else:
                    to_send_ws_data = {
                        "client_id": str(user_obj.id),
                        "data": {
                            "status": "FAILED",
                            "task": "Audio Processing",
                            "audio_request_id": audio_request_id,
                            "detail": "Unknown Error Occurred or Note Deleted",
                            "note_id": notes_id,
                            "note_name": note_name,
                            "workspace_id": workspace_id
                        }
                    }
                    print(to_send_ws_data)
                    redis_publisher_serv(channel=str(user_obj.id), data=to_send_ws_data)
            else:
                """WRONG FILE FORMAT"""
                StorageServices().delete_blob(container_name=data["container_name"], blob_name=file_name)
                print("BAD FILE")
                print(audio_request_id)
                to_send_ws_data = {
                    "client_id": str(user_obj.id),
                    "data": {
                        "status": "FAILED",
                        "task": "Audio Processing",
                        "audio_request_id": audio_request_id,
                        "detail": "BAD FILE SUPPORTED TYPE or MAL FORMED FILE STRUCTURE",
                        "note_id": notes_id,
                        "note_name": note_name,
                        "workspace_id": workspace_id
                    }
                }
                print(to_send_ws_data)
                redis_publisher_serv(channel=str(user_obj.id), data=to_send_ws_data)
        else:
            print("celery task called")
            app.send_task("tasks.audio_process_celery_task.audio_preprocess",
                          queue="stt_queue",
                          kwargs={
                              "file_url": str(url),
                              "note_id": str(notes_id),
                              "file_name": str(file_name),
                              "blob_size": blob_size,
                              "audio_request_id": audio_request_id,
                              "container_name": data["container_name"],
                              "original_file_name": original_file_name,
                              "y_axis": y_axis,
                              "user_id": str(user_obj.id),
                              "workspace_id": workspace_id,
                              "note_name": note_name
                          })
