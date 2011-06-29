# -*- coding: utf-8 -*-

import datetime

from cotufa import db


class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    cover = db.Column(db.Binary, nullable=True, default=None)
    
    created_on = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    seen_on = db.Column(db.Date, nullable=True, default=None)

    rating = db.Column(db.Integer, nullable=False, default=0) # 1 to 3
    
    notes = db.Column(db.UnicodeText, nullable=True, default=None)
    
    @property
    def directors(self):
        return [x.person for x in self.people if x.role_type == 'director']
        
    @property
    def cast(self):
        return [x for x in self.people if x.role_type == 'cast']


class Person(db.Model):
    __tablename__ = 'persons'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255), nullable=False)

    @classmethod
    def get_or_create(cls, id, name):
        id_ = int(id)
        p = db.session.query(Person).filter_by(id=id_).first()
        
        if p is None:
            p = cls(id=id_, name=name)
            db.session.add(p)
            db.session.commit()
        
        return p
    

class MovieRole(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey(Person.id), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id), nullable=False)
    
    role_type = db.Column(db.Unicode(10), nullable=False, default=u'cast') # writer, director, cast

    character = db.Column(db.Unicode(255), nullable=True, default=None)
    
    movie = db.relationship('Movie', backref=db.backref('people'))
    person = db.relationship('Person', backref=db.backref('roles'))
