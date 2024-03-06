from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import validates
import re
# from flask_bcrypt import Bcrypt 
# from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    event_time = db.Column(db.DateTime)
    venue_name  = db.Column(db.String)
    location = db.Column(db.String)
    description = db.Column(db.String)
    event_type = db.Column(db.String)
    # relationship with venue

    # relationship with organiser

class Ticket (db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    ticket_type = db.Column(db.String)
    price = db.Column(db.Integer)
    purchase_date = db.Column(db.DateTime)
    Ticketnumber = db.Column(db.Integer)
    # relationship with event

    # relationship with user

class Testimonial(db.Model):
    __tablename__ = 'testimonials'

    id = db.Column(db.Integer, primary_key = True)
    customer_name = db.Column(db.String)
    customer_title = db.Column(db.String)
    review = db.Column(db.String)
    # rating = db.Column(db.Integer)

    # def serialize(self):
    #     return {
    #         'id':self.id,
    #         'customer_name': self.customer_name,
    #         'review': self.review,
    #         'rating': self.rating
    #     }

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String)
    email = db.Column(db.String)
    message = db.Column(db.String)
    

    # one to many -- user  to  event
        # one to many -- event to ticket
        # one to many -- event to ticket 