from database import db

class DataModel(db.Model):
    __tablename__ = "rbz_api"
    id = db.Column('Id', db.Integer, primary_key=True, autoincrement=True)
    request = db.Column('Request', db.String)
    response = db.Column('Response', db.String)
    accessTime = db.Column('AccessTime', db.TIMESTAMP)
    parentId = db.Column('ParentId', db.Integer)

    def __init__(self, request, response, parentId):
        self.request = request
        self.response = response
        self.parentId = parentId

class DeviceModel(db.Model):
    __tablename__ = "device"
    uuid = db.Column('uuid', db.String, primary_key=True)
    user_id = db.Column('user_id', db.String)

    def __init__(self, uuid, user_id):
        self.uuid = uuid
        self.user_id = user_id

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column('id',  db.Integer, primary_key=True, autoincrement=True)
    username = db.Column('username', db.String)
    email = db.Column('email', db.String)
    password = db.Column('password', db.String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class BackupModel(db.Model):
    __tablename__ = "backup_data"
    id = db.Column('id',  db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer)
    history = db.Column('history', db.String)
    rating = db.Column('rating', db.String)
    favourite = db.Column('favourite', db.String)

    def __init__(self, user_id, history, rating, favourite):
        self.user_id = user_id
        self.history = history
        self.rating = rating
        self.favourite = favourite