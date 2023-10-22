#!/usr/bin/python3
"""DB storage"""


from os import getenv
from models.base_model import Base
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """Connects to MySQL DB"""
    __engine = None
    __session = None

    def __init__(self):
        """Init DB object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Check db session"""
        obj_dict = {}
        for class_name in classes:
            if cls is None or cls is classes[class_name] or cls is class_name:
                objs_list = self.__session.query(classes[class_name]).all()
                for obj in objs_list:
                    key = obj.__class__.__name__ + '.' + obj.id
                    obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add to current session"""
        self.__session.add(obj)

    def save(self):
        """Commit changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from session, if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reads data from DB"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session

    def close(self):
        """Closes the current session."""
        self.__session.close()
