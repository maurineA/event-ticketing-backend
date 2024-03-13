from models import db,Event,Ticket,Order,User,Testimonial
from app import app
from random import choice as rc
from datetime import datetime, time

with app.app_context():
    Event.query.delete()
    Ticket.query.delete()
    Order.query.delete()
    User.query.delete()
    Testimonial.query.delete()


    users =[ 
        {'username':'clement','email':'clementmacharia62@gmail.com','contact':'07438783484','password':'clement'},
        {'username':'jane','email':'janemacharia62@gmail.com','contact':'07456783484','password':'jane123'},
        {'username':'wambui','email':'wambui@gmail.com','contact':'07456783484','password':'wambui123'},


    ]

    for user_data in users:
        new_user= User(**user_data)
        db.session.add(new_user)
        db.session.commit()

    event = [
        {'event_name':'Wedding','start_date':'2024-11-11','end_date':'2024-1-11','event_time':'8:00 AM','venue_name':'Uhuru Park','location':'Nairobi,Kenya','description':'wedding','event_type':'pysical'},
        {'event_name':'Amapiano','start_date':'2024-12-11','end_date':'2024-11-11','event_time':'9:00 PM','venue_name':'Ngong Race Course','location':'Nairobi,Kenya','description':'Amapiano','event_type':'pysical'},
        {'event_name':'Festival','start_date':'2024-12-11','end_date':'2024-11-11','event_time':'10:00 PM','venue_name':'Nairobi National Park','location':'Nairobi,Kenya','description':'Festival','event_type':'pysical'}

    ]

    # user_id = rc(User.query.all()).id

# Create and add events to the database
    for event_data in event:
        event_data['start_date'] = datetime.strptime(event_data['start_date'], '%Y-%m-%d').date()
        event_data['end_date'] = datetime.strptime(event_data['end_date'], '%Y-%m-%d').date()
        event_data['event_time'] = datetime.strptime(event_data['event_time'], '%I:%M %p').time()

        new_event = Event( **event_data)
        db.session.add(new_event)

    # Commit the changes
    db.session.commit()

    # seed data for tickets
    ticket = [
        {'ticket_type':'VVIP','price':100,'quantity':100},
        {'ticket_type':'VIP','price':100,'quantity':70},
        {'ticket_type':'Regular','price':50,'quantity':1000},
        # {'ticket_type':'Student','price':25,'quantity':100}
    ]
    for ticket_data in ticket:
        new_ticket = Ticket(**ticket_data)
        new_ticket.event_id = rc(Event.query.all()).id
        new_ticket.user_id = rc(User.query.all()).id
        # new_ticket.order_id = rc(Order.query.all()).id
        db.session.add(new_ticket)
        db.session.commit()

    testimonial = [
        {'customer_image':'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NTN8fHBlb3BsZXxlbnwwfHwwfHx8MA%3D%3D','customer_name':'james kamau','customer_title':'CEO Amapiano Group','review':'The website made it very easy for our customers to purchase their tickets.'},
        {'customer_image':'https://images.pexels.com/photos/1239291/pexels-photo-1239291.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1','customer_name':'jane doe','customer_title':'CEO Radio Africa','review': 'The websites ticketing features simplified ticket sales and tracking. Great experience!'},
        {'customer_image':'https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg','customer_name':'wambui','customer_title':'CEO Kenya Airways','review': 'The websites promotion tools increased our events visibility. Impressed with the results!'}
    ]
    for testimonial_data in testimonial:
        new_testimonial = Testimonial(**testimonial_data)
        db.session.add(new_testimonial)
        db.session.commit()


print( "🦸‍♀️ Done seeding!")


