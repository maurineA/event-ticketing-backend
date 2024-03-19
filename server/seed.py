from models import db,Event,Ticket,Order,User,Testimonial
from app import app
from random import choice as rc
from datetime import datetime

with app.app_context():
    Event.query.delete()
    Ticket.query.delete()
    Order.query.delete()
    User.query.delete()
    Testimonial.query.delete()


    users =[ 
        {'username':'clement','email':'clementmacharia62@gmail.com','contact':'074387834','password':'clement','is_admin':True},
        {'username':'jane','email':'janemacharia62@gmail.com','contact':'074567834','password':'jane123'},
        {'username':'wambui','email':'wambui@gmail.com','contact':'074567834','password':'wambui123'},


    ]

    for user_data in users:
        new_user= User(**user_data)
        db.session.add(new_user)
        db.session.commit()

    event = [
        {'event_image':"https://launion.gov.ph/wp-content/uploads/2023/03/334721137_1437693610368993_7828899826958531789_n.jpg",'event_name':'COLORFEST','start_date':'2024-11-11','end_date':'2024-03-11','event_time':'8:00 AM','venue_name':'Uhuru Park','location':'Nairobi','description':'Dive into Color Fest - a vibrant celebration of music, art, and colorful fun! Secure your ticket for an unforgettable day of joy and unity','event_type':'pysical'},
        {'event_image':"https://static.toiimg.com/thumb/msid-87392351,imgsize-92086,width-400,resizemode-4/87392351.jpg",'event_name':'HALLOWEEN','start_date':'2024-05-11','end_date':'2024-05-11','event_time':'9:00 PM','venue_name':'Ngong Race Course','location':'Nairobi','description':'Embrace the chills at Halloween Fest: haunted houses, live spooky performances, and a grand costume contest await! Grab your tickets for a night of frightful delight','event_type':'pysical'},
        {'event_image':"https://wrc.enhance.diagnal.com/resources/images/eyJrZXkiOiJodHRwczovL2VuaGFuY2Utc3RvcmFnZS1zdGFjay1wcm9kLXdyY21lZGlhZmlsZXN0b3JhZ2UtZzN6MmhnM3Vyd2ZmLnMzLmFtYXpvbmF3cy5jb20vYmE1ZWU1ODYtZmZmYi00M2UyLTlhMWUtYjE1ODUxZjFlZjA1X3dyY2tlbnlhMjAyNC1rb3BpZS5qcGciLCJ0aW1lc3RhbXAiOiIyMDI0LTAxLTMxVDA5OjE3OjM5LjIxOVoiLCJlZGl0cyI6eyJleHRyYWN0Ijp7ImxlZnQiOjAsInRvcCI6MCwid2lkdGgiOjE5MTAsImhlaWdodCI6MTA4MH0sInJlc2l6ZSI6eyJ3aWR0aCI6NzIwLCJoZWlnaHQiOjQwNX0sImpwZWciOnsicXVhbGl0eSI6MTAwfX19/ba5ee586-fffb-43e2-9a1e-b15851f1ef05_wrckenya2024-kopie.jpg",'event_name':'RALLY','start_date':'2024-06-10','end_date':'2024-06-11','event_time':'10:00 PM','venue_name':'Mombasa show Grounds','location':'Mombasa','description':'Gear up for the thrill at the Ultimate Rally Event: high-speed races and automotive showcases! Secure your spot for adrenaline-packed action','event_type':'pysical'},
        {'event_image':"https://www.queensu.ca/gazette/sites/gazettewww/files/assets/CONVO%20-%20music%20festival%20Glastonbury%20james-genchi-APJ6MvCZefM-unsplash.jpg",'event_name':'MUSIC','start_date':'2024-12-11','end_date':'2024-11-11','event_time':'10:00 PM','venue_name':'Kakamega show grounds','location':'Kakamega','description': 'Join the beat at Music Extravaganza: a night of live performances from top artists! Get your tickets for an unforgettable journey through sound.','event_type':'pysical'},
        {'event_image':"https://www.tourism.go.ke/wp-content/uploads/2023/08/IMG_6728.jpeg",'event_name':'CULTURAL FEST','start_date':'2024-10-11','end_date':'2024-10-11','event_time':'10:00 PM','venue_name':'Kiambu show grounds','location':'Kiambu','description':'Explore the world at Global Culture Fest: music, dance, art, and culinary wonders await! Secure your tickets for a vibrant celebration of diversity.','event_type':'pysical'},
        {'event_image':"https://i0.wp.com/mtltimes.ca/wp-content/uploads/2022/06/Thousands-of-Montrealers-will-join-us-at-the-clock-tower-situated-at-the-Old-Port-of-Montre%CC%81al-for-a-4-day-celebration-Montreal-Street-food-festival-2022..jpg?resize=1024%2C532&ssl=1",'event_name':'STREET FOOD FEST','start_date': '2024-07-10','end_date': '2024-07-10', 'event_time': '8:00 AM','venue_name': 'Street Food Festival','venue_name': 'Street Food Festival',     'description': 'Feast at the Street Food Festival: A culinary journey of global tastes and local delights! Secure your tickets for an epicurean adventure.','event_type': 'pysical'},
        {'event_image':"https://makueni.go.ke/sandbox/site/files/2023/03/Farmers-Exchange-Expo-Makueni-County.jpg",'event_name':"AGRI TECH EVENT","start_date":"2024-08-17","end_date":"2024-08-17","event_time":"8:00 AM","venue_name":"AgriTech Event","location":"Makueni","description":"Dive into innovation at the AgriTech Event, where technology transforms sustainable farming.","event_type":"pysical"},
        {'event_image':"https://imageio.forbes.com/specials-images/imageserve/64e8effc2eb2f509720eda00/974x548.jpg?format=jpg&height=548&width=974&fit=bounds",'event_name': 'NFL EVENT','description': 'Immerse yourself in the electric atmosphere of NFL action, where grit meets grace under the stadium lights, and every moment is a heartbeat away from history.','start_date': '2024-09-10','end_date': '2024-09-10','venue_name': 'NFL Stadium','event_time': '8:00 AM','location': 'Nairobi', 'event_type': 'pysical'},
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


