from models import db,Event,Ticket,Order,User
from app import app

with app.app_context():
    Event.query.delete()
    Ticket.query.delete()
    Order.query.delete()
    User.query.delete()


    users =[ 
        {'username':'clement','email':'clementmacharia62@gmail.com','password':'clement'},
        {'username':'jane','email':'janemacharia62@gmail.com','password':'jane123'}

    ]

    for user_data in users:
        new_user= User(**user_data)
        db.session.add(new_user)
        db.session.commit()
 


