"""Module to setup our DB Connection."""

# disable invalid name warnings for this file
# pylint: disable=C

# IMPORT STANDARD LIBS
import time

# IMPORT THIRD PARTY LIBS
import sqlalchemy
import flask_sqlalchemy
# from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy


class SQLAlchemy(flask_sqlalchemy.SQLAlchemy):

    # https://github.com/pallets/flask-sqlalchemy/issues/589#issuecomment-361075700
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(app, options)
        options["pool_pre_ping"] = True

    def wait_for_connection(self, max_retry=10):
        for i in range(max_retry):
            try:
                self.session.execute('SELECT 1')
            except Exception as e:
                print("waiting for connection: {}/{}".format(i, max_retry))
                time.sleep(0.1)
            else:
                return True

        return False

    def get_or_create(self, obj_cls, commit=True, **kwargs):
        obj = obj_cls.query.filter_by(**kwargs).first()
        if not obj:
            obj = obj_cls(**kwargs)
            self.session.add(obj)

            if commit:
                self.session.commit()

        return obj


class Model(flask_sqlalchemy.Model):

    @classmethod
    def get_or_create(cls, **kwargs):
        obj = cls.query.filter_by(**kwargs).first()
        if not obj:
            obj = cls(**kwargs)
        return obj

    get = get_or_create


    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def session(self):
        return sqlalchemy.orm.session.object_session(self)

    """
    @classmethod
    def get_or_create(self, obj_cls, add=True, commit=True, **kwargs):
        obj = obj_cls.query.filter_by(**kwargs).first()
            self.session.add(obj)

            if commit:
                self.session.commit()

        return obj
    """


db = SQLAlchemy(model_class=Model)


def init_app(app):
    db.init_app(app)  # init SQLAlchemy
    # db.wait_for_connection()


