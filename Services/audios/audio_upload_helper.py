from db_models.models import NotesModel
from db_models.models.audio_model import Audio
from db_models.models.audio_results_model import AudioResultsModel
from db_models.models.tags_model import TagModel


def save_to_db(stt_data, note_obj, name, y_axis, url, blob_name, file_size, note_name):
    if "transcribe" in stt_data:
        stt = stt_data["transcribe"]
        f_align_data = stt_data["f_align"]
    else:
        stt = None
        f_align_data = None
    if "sound_recog_results" in stt_data:
        sound_recog = stt_data["sound_recog_results"]
    else:
        sound_recog = None
    audio_model_obj = Audio(notes_id=note_obj, user_id=note_obj.user_id, name=name, y_axis=y_axis)
    audio_model_obj.save()
    audio_results_obj = AudioResultsModel(
        user_id=note_obj.user_id,
        notes_id=note_obj,
        audio_id=audio_model_obj,
        url=url,
        blob_name=blob_name,
        stt=stt,
        forced_alignment_data=f_align_data,
        sound_recog_results=sound_recog,
        blob_size=file_size
    )
    audio_results_obj.save()
    return {"audio_results_obj": audio_results_obj, "audio_obj": audio_model_obj, "note_name": note_name}


def audio_save_to_db(file_size, stt_data, notes_id, url, blob_name, name, y_axis):
    try:
        note_obj = NotesModel.objects.get(id=notes_id)
        return save_to_db(stt_data, note_obj, name, y_axis, url, blob_name, file_size, )
    except NotesModel.DoesNotExist:
        try:
            note_obj = NotesModel.objects.get(id=notes_id)
            return save_to_db(stt_data, note_obj, name, y_axis, url, blob_name, file_size,
                              note_name=note_obj.notes_name)
        except NotesModel.DoesNotExist:
            print("Note Deleted")
            return None
