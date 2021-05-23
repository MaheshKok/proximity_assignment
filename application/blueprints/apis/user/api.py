from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi import ResourceList
from flask_rest_jsonapi import ResourceRelationship

from application.extensions import db
from application.models.user.sql import User
from application.schema.user.schema import UserSchema


# Create resource managers
class UserDetail(ResourceDetail):
    schema = UserSchema
    data_layer = {"session": db.session, "model": User}


class UserList(ResourceList):
    schema = UserSchema
    data_layer = {"session": db.session, "model": User}


class UserRelationship(ResourceRelationship):
    schema = UserSchema
    data_layer = {"session": db.session, "model": User}
