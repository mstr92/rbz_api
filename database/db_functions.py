##################################################################
# DATABASE
##################################################################
from database import db
from database.model import DataModel
from datetime import datetime, timedelta
from sqlalchemy import exc, create_engine
from settings import SQLALCHEMY_DATABASE_URI

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
                                   DataModel.accessTime > datetime.today() - timedelta(days=7)).all()
        if len(d) == 0:
            return None, None
        else:
            return d[0].id, d[0].response

    except exc.SQLAlchemyError:
        print("No entry in Database")
        return None, None


def get_entry(id):
    try:
        return DataModel.query.filter(DataModel.id == id).one()
    except exc.SQLAlchemyError:
        print("No entry in Database")
        return None


def set_response(id, retval):
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        connection = engine.connect()
        trans = connection.begin()
        connection.execute('UPDATE rbz_api SET Response = "' + retval + '" WHERE Id = "' + str(id) + '";')
        trans.commit()
        connection.close()

    except exc.SQLAlchemyError:
        print("No entry in Database")
        return None