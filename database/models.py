import peewee
import os

path = os.path.abspath(os.path.join('database', 'db.sqlite3'))
db = peewee.SqliteDatabase(path)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class UserInfo(BaseModel):
    city_name = peewee.CharField(max_length=40, null=True)
    latitude = peewee.FloatField(null=True)
    longitude = peewee.FloatField(null=True)
    city_id = peewee.CharField(null=True)
    user_id = peewee.BigIntegerField(null=False, unique=True)


with db:
    if not UserInfo.table_exists():
        UserInfo.create_table()
