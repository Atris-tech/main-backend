def generate_typsns_data(obj, notes_name=False, summary=False, clean_text=False):
    print(obj.last_edited_date)
    data = {
        "id": str(obj.id),
        "date": int(obj.last_edited_date.timestamp()),
        "user_id": str(obj.user_id.id)
    }
    if notes_name:
        data["summary"] = summary
        data["clean_text"] = clean_text
        data["notes_name"] = notes_name
        return data
