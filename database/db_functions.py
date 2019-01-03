##################################################################
# DATABASE
##################################################################
import time
from database import db
from database.model import DataModel, GenreModel
from datetime import datetime, timedelta
from sqlalchemy import exc, create_engine, MetaData, Table, Column, Integer, String,TIMESTAMP, text
from settings import SQLALCHEMY_DATABASE_URI, EXPIRE_DAYS


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

def get_genre(id):
    try:
        db.session.commit()
        return GenreModel.query.filter(GenreModel.id == id).one()
    except exc.SQLAlchemyError:
        print("No entry in Database")
        return None

def set_response(id, retval, retry):
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        engine.execute("UPDATE rbz_api SET Response = %s WHERE Id = %s", (retval, str(id)))

    except exc.SQLAlchemyError:
        print("No entry in Database with ID: " + str(id))
        if retry:
            set_response(id, retval, False)


def create_table_if_not_exists():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    if not engine.dialect.has_table(engine, "rbz_api"):
        metadata = MetaData(engine)
        table = Table('rbz_api', metadata,
                      Column('Id', Integer, primary_key=True, autoincrement=True),
                      Column('Request', String(10000)),
                      Column('Response', String(10000)),
                      Column('AccessTime', TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
                      Column('ParentId', Integer))
        metadata.create_all()
