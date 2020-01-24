from service import es_db


def edit_password(user_id, password):
    return es_db.edit_password(user_id, password)
