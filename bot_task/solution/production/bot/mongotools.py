import pymongo


def get_db():
    client = pymongo.MongoClient('mongodb://root:password@mongo:27017/')
    db = client.nti
    # client = pymongo.MongoClient('mongodb://heroku_2n5xgpck:hfoqb10p4b1968cv42nbrsrlef@ds031359.mlab.com:31359/heroku_2n5xgpck?retryWrites=false')
    # db = client.heroku_2n5xgpck
    return db.personal_data_bot


default_user = {'alias':"",
                'name': "",
                'surname': "",
                'state': 0}


def create_new_user(db, alias, name="", surname="", state=0):
    user = default_user.copy()
    user['alias'] = normalize_alias(alias)
    user['name'] = name
    user['surname'] = surname
    user['state'] = state
    db.insert_one(user)
    return user

def get_user(db, alias):
    """
    Returns all information about user
    """
    for user_iter in db.find({'alias': normalize_alias(alias)}):
        return user_iter
        
    return None


def user_in_database(db, alias):
    return not get_user(db, alias) is None


def update(db, alias, name=None, surname=None, state=None):
    new_user_options = {}
    for option_name, option in zip(['name', 'surname', 'state'],
                                   [name, surname, state]):
        if not option is None:
            new_user_options[option_name] = option
    
    
    db.update_one({'alias': normalize_alias(alias)}, {'$set': new_user_options})

def normalize_alias(alias):
    return '@' + alias.replace('@', '')

if __name__ == "__main__":
    pass