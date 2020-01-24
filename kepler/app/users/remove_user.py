from service import es_db


def delete_user(user_id):
    return es_db.delete_user(user_id)
