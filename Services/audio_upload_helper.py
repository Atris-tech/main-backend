import uuid
from db_models.models.audio_model import Audio


def audio_save_to_db(file_size, stt_data, note_obj, url):
    if "transcribe" in stt_data:
        stt = stt_data["transcribe"]
        f_align_data = stt_data["f_align"]
    sound_recog = stt_data["sound_recog_results"]
    audio_model_obj = Audio(url=url, blob_name=str(uuid.uuid4()) + ".wav", blob_size=file_size,
                            sound_recog_results=sound_recog, forced_alignment_data=f_align_data, stt=stt)
    audio_model_obj.save()
    note_obj.audios.append(audio_model_obj)
    note_obj.save()
