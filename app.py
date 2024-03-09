from models import db,User,Event,Ticket,Contact,Testimonial, datetime, Order
from flask_migrate import Migrate
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = b'\xb2\xd3B\xb9 \xab\xc0By\x13\x10\x84\xb7M!\x11'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app)
jwt = JWTManager()
jwt.init_app(app)

# perform other rest routes for  events tickets testimonials and contacts

    
class AddEvent(Resource):
     
    def post(self):

        event_name = request.get_json()['event_name']
        start_date_str = request.get_json()['start_date']
        end_date_str = request.get_json()['end_date']
        event_time_str = request.get_json()['event_time']
        venue_name = request.get_json()['venue_name']
        location = request.get_json()['location']
        description = request.get_json()['description']
        event_type = request.get_json()['event_type']
        

        # Convert date strings to Python date objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

         # Convert time string to Python time object
        event_time = datetime.strptime(event_time_str, '%H:%M:%S').time()


        new_event = Event(
            
            event_name=event_name,
            start_date=start_date,
            end_date=end_date,
            event_time=event_time,
            venue_name=venue_name,
            location=location,
            description=description,
            event_type=event_type
            
        )

        db.session.add(new_event)
        db.session.commit()

        response_dict = new_event.to_dict()

        # Convert time object to string before serializing
        response_dict['event_time'] = event_time_str

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response
    
    
    def get(self, id):
        response_dict_list = [event.serialize() for event in Event.query.filter_by(id=id).all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response
    

    
class BuyTicket(Resource):
     
    def post(self):
        ticket_type = request.get_json()['ticket_type']
        price = request.get_json()['price']
        # purchase_date_str = request.get_json()['purchase_date']
        quantity = request.get_json()['quantity']

        # # Convert date strings to Python date objects
        # purchase_date = datetime.strptime(purchase_date_str, '%Y-%m-%d').date()


        new_ticket = Ticket(
            
            ticket_type=ticket_type,
            price=price,
            # purchase_date=purchase_date,
            quantity=quantity

        )

        db.session.add(new_ticket)
        db.session.commit()

        response_dict = new_ticket.to_dict()

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response
    
    
    def get(self, id):
        response_dict_list = [tickets.serialize() for tickets in Ticket.query.filter_by(id=id).all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response

class GetTestimonials(Resource):
    def get(self):
        response_dict_list = [testimonials.serialize() for testimonials in Testimonial.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response

class GetOrder(Resource):
    def get(self, id):
        response_dict_list = [orders.serialize() for orders in Order.query.filter_by(id=id).all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response
    

class PostContact(Resource):
    def post(self):
        full_name = request.get_json()['full_name']
        email = request.get_json()['email']
        message = request.get_json()['message']

        new_contact  = Contact(
           
            full_name=full_name,
            email=email,
            message=message
        )

        db.session.add(new_contact)
        db.session.commit()

        response_dict = new_contact.to_dict()

       

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response






api.add_resource(GetTestimonials, '/testimonials')
api.add_resource(BuyTicket, '/tickets/<int:id>')
api.add_resource(GetOrder, '/orders/<int:id>')
api.add_resource(AddEvent, '/events/<int:id>')
api.add_resource(PostContact, '/contacts')





if __name__ == '__main__':
    app.run(port=5555,debug=True)

