from service import es_db


def sign_up_service(name, email, mobile, address, password):
    return es_db.add_new_user(name, email, mobile, address, password)
