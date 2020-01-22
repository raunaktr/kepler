from service import es_db


def sign_in_service(email, password):
    return es_db.auth(email, password)
