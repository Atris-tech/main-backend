from db_models.models.audio_model import Audio
from db_models.models import NotesModel


def audio_save_to_db(file_size, stt_data, notes_id, url, blob_name, name, y_axis):
    try:
        note_obj = NotesModel.objects.get(id=notes_id)
        if "transcribe" in stt_data:
            stt = stt_data["transcribe"]
            f_align_data = stt_data["f_align"]
        sound_recog = stt_data["sound_recog_results"]
        audio_model_obj = Audio(notes_id=note_obj, url=url, blob_name=blob_name, blob_size=file_size,
                                sound_recog_results=sound_recog, user_id=note_obj.user_id,
                                forced_alignment_data=f_align_data, stt=stt, name=name, y_axis=y_axis)
        audio_model_obj.save()
        return audio_model_obj
    except NotesModel.DoesNotExist:
        print("Note Deleted")
