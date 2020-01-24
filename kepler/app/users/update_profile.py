from service import es_db


def edit_profile(user_id, name, email, phone, address):
    return es_db.edit_user_details(user_id, name, email, phone, address)
