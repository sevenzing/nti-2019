import pymongo


def get_db():
    client = pymongo.MongoClient('mongodb://root:password@mongo:27017/')
    db = client.nti

    return db.personal_data_bot


default_user = {'chat_id':"",
                'alias':"",
                'name': "",
                'surname': "",
                'state': 0}



def create_new_user(db, chat_id, alias='', name="", surname="", state=0):
    user = default_user.copy()
    user['chat_id'] = chat_id
    user['alias'] = normalize_alias(alias)
    user['name'] = name
    user['surname'] = surname
    user['state'] = state
    db.insert_one(user)
    return user


def get_user(db, information):
    """
    Returns all information about user
    """

    for user_iter in db.find({'alias': normalize_alias(information)}):
        return user_iter

    for user_iter in db.find({'chat_id': information}):
        return user_iter

    
        
    return None


def user_in_database(db, alias):
    return not get_user(db, alias) is None


def update_user(db, chat_id, alias=None, name=None, surname=None, state=None):
    new_user_options = {}
    for option_name, option in zip(['alias', 'name', 'surname', 'state'],
                                   [alias, name, surname, state]):
        if not option is None:
            new_user_options[option_name] = option
    
    
    db.update_one({'chat_id': chat_id}, {'$set': new_user_options})


def normalize_alias(alias):
    return '@' + alias.replace('@', '')

if __name__ == "__main__":
    pass