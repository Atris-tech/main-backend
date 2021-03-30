from Services.notes.date_time_string_to_unix_time import convert_dt_to_unixt


def generate_typsns_data(obj, notes=False, summary=False, clean_text=False):
    data = {
        "id": str(obj.id),
        "date": convert_dt_to_unixt(obj.last_edited_date),
        "user_id": str(obj.user_id)
    }
    if notes:
        data["summary"] = summary
        data["clean_text"] = clean_text
        return data
