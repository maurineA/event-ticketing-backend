from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
import re
from flask_bcrypt import Bcrypt 
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import time,datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model,SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    contact = db.Column(db.Integer )
    hashed_password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)    


    # relationship with event
    # events = db.relationship('Event', backref='user')
    # relationship with ticket
    tickets = db.relationship('Ticket', backref='user')
    # relationship with order
    orders = db.relationship('Order', backref='user')

    # validates email
    @validates('email')
    def validate_email(self, key, email):
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'    
        if not re.match(email_pattern, email):
            raise ValueError('Invalid email format')
        
        return email
        
     # Password getter and setter methods
    @hybrid_property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, plain_text_password):
        self.hashed_password = bcrypt.generate_password_hash(
            plain_text_password.encode('utf-8')).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.hashed_password, attempted_password.encode('utf-8'))
    

    # serialize
    def serialize(self):
        return {
            'id': self.id,
            'username':self.username,
            'email': self.email,
            'contact':self.contact,
            'is_admin':self.is_admin
        }
    
class Company(db.Model, SerializerMixin):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String, nullable=False, unique=True)
    company_email = db.Column(db.String, nullable=False, unique=True)
    company_contact = db.Column(db.Integer)
    hashed_password = db.Column(db.String, nullable=False)

    # relationship with events
    events = db.relationship('Event', backref='company')
    # # relationship with ticket
    # tickets = db.relationship('Ticket', backref='company')

    # Password getter and setter methods
    @hybrid_property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, plain_text_password):
        self.hashed_password = bcrypt.generate_password_hash(
            plain_text_password.encode('utf-8')).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.hashed_password, attempted_password.encode('utf-8'))

    # serialize
    def serialize(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'company_email': self.company_email,
            'company_contact': self.company_contact
        }


class Event(db.Model,SerializerMixin):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    event_time = db.Column(db.Time)
    venue_name  = db.Column(db.String)
    location = db.Column(db.String)
    description = db.Column(db.String)
    event_type = db.Column(db.String)
    

    # relationship with ticket
    tickets = db.relationship('Ticket', backref='event')
    # relationship to user
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # relationship with order
    orders = db.relationship('Order', backref='event')
    # relationship with company
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    # event_time_str = self.event_time.strftime('%H:%M:%S')

    # serialize 
    def serialize(self):
          # Fetch the quantity of tickets available for each ticket type category for this event
        ticket_categories = {'VVIP': 0, 'VIP': 0, 'Regular': 0}

        # Iterate over each ticket and increment the count for its category
        tickets = Ticket.query.filter_by(event_id=self.id).all()
        for ticket in tickets:
            if ticket.ticket_type == 'vvip':
                ticket_categories['VVIP'] += ticket.quantity
            elif ticket.ticket_type == 'vip':
                ticket_categories['VIP'] += ticket.quantity
            elif ticket.ticket_type == 'regular':
                ticket_categories['Regular'] += ticket.quantity

        return {
            'id': self.id,
            'event_name': self.event_name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'event_time': str(self.event_time), 
            'venue_name': self.venue_name,       
            'location': self.location,
            'description': self.description,
            'event_type': self.event_type,
            'company_id': self.company_id,
            'ticket_categories': ticket_categories
        }
class Ticket (db.Model,SerializerMixin):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    ticket_type = db.Column(db.String)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    
    # relationship with event
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    # relationship with user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # relationship with order
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    
    # serialize
    def serialize(self):
        return {
            'id': self.id,
            'ticket_type': self.ticket_type,
            'price': self.price,
            'quantity': self.quantity,
            'event_id': self.event_id,
            # 'user_id': self.user_id,
            # 'order_id': self.order_id
        }

class Order(db.Model,SerializerMixin):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime)
    total_price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    # relationship with ticket
    tickets = db.relationship('Ticket', backref='order')
    # relationship with user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # relationship with event
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def serialize(self):
        return {
            'id': self.id,
            'order_date': self.order_date,
            'total_price': self.total_price,
            'quantity': self.quantity
        }
    


class Testimonial(db.Model,SerializerMixin):
    __tablename__ = 'testimonials'

    id = db.Column(db.Integer, primary_key = True)
    customer_image = db.Column(db.String)
    customer_name = db.Column(db.String)
    customer_title = db.Column(db.String)
    review = db.Column(db.String)
    # rating = db.Column(db.Integer)

    def serialize(self):
        return {
            'id':self.id,
            'customer_image':self.customer_image,
            'customer_name': self.customer_name,
            'customer_title':self.customer_title,
            'review': self.review,
            # 'rating': self.rating
        }
    
    

class Contact(db.Model,SerializerMixin):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String)
    email = db.Column(db.String)
    message = db.Column(db.String)


    def serialize(self):
        return {
            'id':self.id,
            'full_name': self.full_name,
            'email': self.email,
            'message': self.message
        }
    

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(), nullable=True)
    created_at = db.Column(db.DateTime , default=datetime.now())

    def __repr__ (self):
        return f"<tokem {self.jti}>"