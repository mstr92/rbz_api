##################################################################
# DATABASE
##################################################################
import time
import logging
from database import db
from database.model import DataModel, DeviceModel, UserModel, BackupModel
from datetime import datetime, timedelta
from sqlalchemy import exc, create_engine, MetaData, Table, Column, Integer, String, TIMESTAMP, text
from settings import SQLALCHEMY_DATABASE_URI, EXPIRE_DAYS
###################################################################################
# API - Functions
###################################################################################
def create_entry(request, response, parentId):
    post = DataModel(request, response, parentId)
    db.session.add(post)
    db.session.flush()
    db.session.commit()
    return post.id

def check_if_entry_exists(data):
    try:
        d = DataModel.query.filter(DataModel.request == data,
                                   DataModel.parentId == None,
                                   DataModel.accessTime > datetime.today() - timedelta(days=EXPIRE_DAYS)).all()
        if len(d) == 0:
            return None, None
        else:
            return d[0].id, d[0].response

    except exc.SQLAlchemyError:
        print("No entry in Database")
        return None, None

def get_entry(id):
    try:
        db.session.commit()
        return DataModel.query.filter(DataModel.id == id).one()
    except exc.SQLAlchemyError:
        print("No entry in Database")
        return None

def set_response(id, retval, retry):
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        engine.execute("UPDATE rbz_api SET Response = %s WHERE Id = %s", (retval, str(id)))

    except exc.SQLAlchemyError(e):
        print("No entry in Database with ID: " + str(id))
        print(e)
        if retry:
            set_response(id, retval, False)

###################################################################################
# Movie and MetaData
###################################################################################
def get_movie(text):
    try:
        search_query = "%" + str(text) + "%"
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        result = engine.execute(
            "SELECT id, ttid, title, year FROM movie WHERE LOWER(title) LIKE LOWER(%s) ORDER BY rating_rank DESC LIMIT 5",
            search_query)
        return result

    except exc.SQLAlchemyError:
        print("No entry in Database")
        return None

def get_genre(text):
    try:
        search_query = "%" + str(text) + "%"
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        result = engine.execute("SELECT id,genrename FROM genre WHERE LOWER(genrename) LIKE LOWER(%s) LIMIT 5",
                                search_query)
        return result

    except exc.SQLAlchemyError:
        print("No entry in Database")
        return None

def get_person(text):
    try:
        search_query = "%" + str(text) + "%"
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        result = engine.execute(
            "SELECT id, first_name, last_name FROM person WHERE CONCAT(LOWER(first_name),  ' ', LOWER(last_name)) LIKE LOWER(%s) OR CONCAT(LOWER(last_name),  ' ', LOWER(first_name)) LIKE LOWER(%s) LIMIT 5",
            (search_query, search_query))
        return result

    except exc.SQLAlchemyError:
        print("No entry in Database")
        return None

###################################################################################
# General Functions
###################################################################################
def set_uuid(uuid):
    try:
        post = DeviceModel(uuid, None)
        db.session.add(post)
        db.session.flush()
        db.session.commit()
        return True

    except exc.SQLAlchemyError as e:
        print("No entry in Database")
        print(e)
        return False


def set_user(username, email, password):
    try:
        post = UserModel(username,email,password)
        db.session.add(post)
        db.session.flush()
        db.session.commit()
        return True

    except exc.SQLAlchemyError as e:
        print("No entry in Database")
        print(e)
        return False

def get_user(username):
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        result = engine.execute(
            "SELECT id, username, email, password FROM user WHERE username = %s", username)
        return result
    except exc.SQLAlchemyError as e :
        print("No entry in Database")
        print(e)
        return None

def set_backup(user_id, history, rating, favourite):
    try:
        backupObject = BackupModel.query.filter(BackupModel.user_id == user_id).first()
        if  backupObject == None:
            post = BackupModel(user_id,history,rating,favourite)
            db.session.add(post)
            db.session.flush()
        else:
            if history != '':
                backupObject.history = history
            if rating != '':
                backupObject.rating = rating
            if favourite != '':
                backupObject.favourite = favourite
        db.session.commit()
        return True

    except exc.SQLAlchemyError as e:
        print("No entry in Database")
        print(e)
        return False

def get_backup(user_id):
    try:
        db.session.commit()
        return BackupModel.query.filter(BackupModel.user_id == user_id).one()
    except exc.SQLAlchemyError:
        print("No entry in Database")
        return None