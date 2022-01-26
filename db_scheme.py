from peewee import *

# pragmas={'foreign_keys': 1} - для работы каскадного удаления на sqlite
db = SqliteDatabase('Vahta.db', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    guid = IntegerField(primary_key=True)
    name = CharField()
    birthday = DateField()
    position = CharField()

    class Meta:
        database = db


class Building(BaseModel):
    name = CharField(unique=True)

    class Meta:
        database = db


#
class Key(BaseModel):
    guid = IntegerField(primary_key=True)
    name = CharField()
    build_id = ForeignKeyField(Building, backref='build', on_delete='CASCADE')

    class Meta:
        database = db


#
#
#
class AllowedKeys(BaseModel):
    user = ForeignKeyField(Person, backref='user', on_delete='CASCADE')
    key = ForeignKeyField(Key, backref='key', on_delete='CASCADE')

    class Meta:
        database = db


class KeysHistory(BaseModel):
    date = DateTimeField()
    this_return = BooleanField()
    key = ForeignKeyField(Key, backref='key', on_delete='CASCADE')
    user = ForeignKeyField(Person, backref='user', on_delete='CASCADE', null=False)
    comment = CharField()

    class Meta:
        database = db


db.create_tables([Person, Building, Key, AllowedKeys])
db.create_tables([KeysHistory])
