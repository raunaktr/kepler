from elasticsearch import Elasticsearch
import uuid
import traceback

# declaring Elasticsearch as object. more parameters to be introduced..
es = Elasticsearch()

# this function checks if the connection is established or not
if not es.ping():
    raise ValueError('Connection could not be established.')


# miscellaneous support functions
# es.cluster.health( wait_for_status='yellow', request_timeout=1)

def uuid_generator():
    temp_id = uuid.uuid1()
    return temp_id.hex


##############################
#####Creating a new user######
##############################
def add_new_user(name, email, mobile, address, password):
    try:
        # query DSL for searching if user already exist in auth index.
        auth_check = es.search(index='kepler_auth', body={
            "query": {
                "bool": {
                    "must": {
                        "term": {
                            "email.keyword": email
                        }
                    }
                }
            }
        })

        # if user is found, printing(later to be removed line)
        # obtained result will be a dictionary of list of dictionary
        print(auth_check.get('hits').get('hits'))
        # storing result of the above result in a variable for further
        auth_res = auth_check.get('hits').get('hits')

        if len(auth_res) == 0:
            # now calling the uuid_generator function for creating a unique id for a user
            id_value = uuid_generator()
            # creating a field(document) for user in kepler_auth and kepler_user_details
            user_auth_data = es.index(index='kepler_auth', id=id_value, body={
                "user_id": id_value,
                "email": email,
                "password": password
            })

            user_details_data = es.index(index='kepler_user_details', id=id_value, body={
                "user_id": id_value,
                "name": name,
                "mobile": mobile,
                "address": address
            })

            # printing for the sake of it
            print(user_auth_data)
            print("####################################")
            print(user_details_data)
            print("_____________________________________")
            return "Created new user"
        else:
            return "Already exists"
    except Exception as e:
        traceback.print_exc()
        return "Error occurred: ", str(e)


#######################
#####Authenticator#####
#######################
def auth(email, password):
    try:
        # query DSL for searching if user already exist in auth index.
        auth_check = es.search(index='kepler_auth', body={
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "email.keyword": email
                            }
                        },
                        {
                            "match": {
                                "password.keyword": password
                            }
                        }
                    ]
                }
            }
        })
        auth_res = auth_check.get('hits').get('hits')
        print(auth_res)

        # find it out yourself, will surely tell you anyway, though
        if len(auth_res) != 0:
            init_list = []
            for i in auth_res:
                init_list.append(i.get('_source'))
            return init_list[0]
        else:
            return "Wrong credentials"
    except Exception as e:
        traceback.print_exc()
        return "Error occurred: ", str(e)


##############################################
####Standalone email only checker function####
##############################################
def check_email(email):
    # this is used to check if entered email is correct or not
    try:
        # query DSL for searching if user already exist in auth index.
        auth_check = es.search(index='kepler_auth', body={
            "query": {
                "bool": {
                    "must": {
                        "term": {
                            "email.keyword": email
                        }
                    }
                }
            }
        })

        # if user is found, printing(later to be removed line)
        # obtained result will be a dictionary of list of dictionary
        print(auth_check.get('hits').get('hits'))
        # storing result of the above result in a variable for further
        email_res = auth_check.get('hits').get('hits')

        if len(email_res) != 0:
            init_list = []
            for i in email_res:
                init_list.append(i.get('_source'))
            return init_list[0]
        else:
            return "Wrong credentials"
    except Exception as e:
        traceback.print_exc()
        return "Error occurred: ", str(e)


##############################
####delete user by user_id####
##############################
def delete_user(user_id):
    try:
        check_user = es.search(index='kepler_auth', body={
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "user_id.keyword": user_id
                            }
                        }
                    ]
                }
            }
        })

        obtained_user = check_user.get('hits').get('hits')
        if len(obtained_user) != 0:
            remove_user_from_user_detail = es.delete_by_query(index='kepler_user_details', body={
                "query": {
                    "bool": {
                        "must": [
                            {
                                "term": {
                                    "user_id.keyword": user_id
                                }
                            }
                        ]
                    }
                }
            })
            remove_user_from_auth = es.delete_by_query(index='kepler_auth', body={
                "query": {
                    "bool": {
                        "must": [
                            {
                                "term": {
                                    "user_id.keyword": user_id
                                }
                            }
                        ]
                    }
                }
            })
            print(remove_user_from_user_detail)
            print("###########################")
            print("###########################")
            print(remove_user_from_auth)

        else:
            return "Failed to delete"
            # to be worked upon
    except Exception as e:
        traceback.print_exc()
        return "Error occurred: ", str(e)

#########   TEST FUNCTIONS  #########
# add_new_user('aditya','aditya@email.com','9999999999','bangalore','123')
# auth('raunak@email.com','xoxo')
# check_email('aditya@email.com')
# delete_user('e073a3b43a2d11ea99c6e442a65e9656')
