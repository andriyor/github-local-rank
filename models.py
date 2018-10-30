from mongoengine import *

connect('github-rank')


class Rank(EmbeddedDocument):
    time = DateTimeField()
    position = IntField()
    repositories = IntField()
    forks = IntField()


class User(Document):
    login = StringField(unique=True)
    location = StringField()
    ranks = ListField(EmbeddedDocumentField(Rank))
