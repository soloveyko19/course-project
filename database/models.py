"""
Module with database models
"""

import peewee
import os

path = os.path.abspath(os.path.join("database", "db.sqlite3"))
db = peewee.SqliteDatabase(path)


class BaseModel(peewee.Model):
    """
    Base Model to init the database for a daughter models
    """
    class Meta:
        database = db


class UserInfo(BaseModel):
    """
    Model which contains info about user

    Attributes:
        city_name (CharField): name of selected city
        latitude (FloatField): latitude of selected city
        longitude (FloatField): longitude of selected city
        city_id (CharField): id of selected city in API
        user_id (BigIntegerField): user's telegram id
    """
    city_name = peewee.CharField(max_length=40, null=True)
    latitude = peewee.FloatField(null=True)
    longitude = peewee.FloatField(null=True)
    city_id = peewee.CharField(null=True)
    user_id = peewee.BigIntegerField(null=False, unique=True)


with db:
    if not UserInfo.table_exists():
        UserInfo.create_table()
