def generate_typsns_data(obj, notes_name=False, summary=False, clean_text=False, audio_data=False,
                         ocr_text=False, labels_list=False):
    print(obj.last_edited_date)
    data = {
        "id": str(obj.id),
        "user_id": str(obj.user_id.id)
    }
    if notes_name:
        data["date"] = int(obj.last_edited_date.timestamp())
        data["summary"] = summary
        data["clean_text"] = clean_text
        data["notes_name"] = notes_name
        return data
    else:
        data["notes_id"] = str(obj.notes_id.id)
        data["date"] = int(obj.last_edited_date.timestamp())
        if audio_data:
            data["transcribe"] = audio_data["transcribe"]
            data["sound_recog"] = audio_data["sound_recog_results"]
            data["name"] = obj.name
            print("name")
            print(obj.name)
            return data
        elif ocr_text or labels_list:
            print("ocr_text in tps")
            print(ocr_text)
            print(type(ocr_text))
            data["ocr"] = ocr_text
            data["labels"] = labels_list
            return data



