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


class GenreModel(db.Model):
    __tablename__ = "genre"
    id = db.Column('id', db.Integer, primary_key=True)
    genrename = db.Column('genrename', db.String)

    def __init__(self, genrename):
        self.genrename = genrename