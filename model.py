# -*- coding: utf-8 -*-
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __str__(self):
        return '<table:{0}<<<<{1}>'.format(self.__tablename__, self.name)
    def __repr__(self):
        return self.__str__()

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    users = db.relationship(User, backref='role', lazy='dynamic')

    def __str__(self):
        return '<table:{0}<<<<{1}>'.format(self.__tablename__, self.name)
    def __repr__(self):
        return self.__str__()
