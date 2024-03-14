from models import db,User,Event,Ticket,Contact,Testimonial, datetime, Order,TokenBlocklist,Company
from flask_migrate import Migrate
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity
from auth import auth_bp


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = b'\xb2\xd3B\xb9 \xab\xc0By\x13\x10\x84\xb7M!\x11'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event.db'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 24 * 60 * 60
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app)
jwt = JWTManager()
jwt.init_app(app)

# perform other rest routes for  events tickets testimonials and contacts

# register blueprint from auth
app.register_blueprint(auth_bp, url_prefix='/auth')

#additional claims
@jwt.additional_claims_loader
def make_additional_claims(identity):
    if identity == 'clement':
        return {"is_staff": True}
    return{"is_staff": False}

# jwt error handler
@jwt.expired_token_loader
def expired_token(jwt_header,jwt_data):
    return jsonify({'message': 'The token has expired.','error':'token expired'}), 401

@jwt.invalid_token_loader
def invalid_token(error):
    return jsonify({'message': 'Does not contain a valid token.','error':'invalid token'}), 401

@jwt.unauthorized_loader
def missing_token(error):
    return jsonify({'message': 'Request does not contain an access token.', 'error':'token missing'}), 401


@jwt.token_in_blocklist_loader #check if the jwt is revocked
def token_in_blocklist(jwt_header,jwt_data):
    jti = jwt_data['jti']

    token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()
# if token is none : it will return false 
    return token is not None
        
class AddEvent(Resource):   
    def get(self):
        response_dict_list = [event.serialize() for event in Event.query.all()]
        response = make_response(
            jsonify(response_dict_list),
            200,
        )
        print("printing events")

        return response

    @jwt_required() # company must be logged in to add an event
    def post(self):
        data = request.get_json()
        current_user = get_jwt_identity()
        company = Company.query.filter_by(company_name=current_user).first()
        if not company:
            return {'error': 'Company not found'}, 404
        else:
            start_date_str = data['start_date']
            end_date_str = data['end_date']
            event_time_str = data['event_time']
            event_name = data['event_name']
            location = data['location']
            description = data['description']
            event_type = data['event_type']
            venue_name = data['venue_name']
        
            # Convert date strings to Python date objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            # Convert time string to Python time object
            event_time = datetime.strptime(event_time_str, '%H:%M').time()

            new_event = Event(
                
                event_name=event_name,
                start_date=start_date,
                end_date=end_date,
                event_time=event_time,
                location=location,
                description=description,
                event_type=event_type,
                venue_name = venue_name,
                company_id=company.id
                
            )

            db.session.add(new_event)
            db.session.commit()

            response_dict = new_event.serialize()

            # Convert time object to string before serializing
            response_dict['event_time'] = event_time_str

            response = make_response(
                jsonify(response_dict),
                201,
            )

            return response
        
@app.route('/companyevents', methods=['GET'])
@jwt_required()
def get_company_events():
    current_company_name = get_jwt_identity()
    company = Company.query.filter_by(company_name=current_company_name).first()
    if not company:
        return jsonify({'error': 'Company not found'}), 404

    events = Event.query.filter_by(company_id=company.id).all()
    serialized_events = [event.serialize() for event in events]
    
    return jsonify(serialized_events), 200


class BuyTicket(Resource):
    @jwt_required() #user must be logged in to buy a ticket
    def post(self):
        data = request.get_json()
        current_user = get_jwt_identity()
        company = Company.query.filter_by(company_name=current_user).first()
        event = Event.query.filter_by(event_name=data['event_name']).first()
        if not company:
            return {'error': 'User not found'}, 404
        elif not event:
            return {'error': 'Event not found'}, 404
        else:
            ticket_type = data['ticket_type']
            price = data['price']
            quantity = data['quantity']

            new_ticket = Ticket( 
                ticket_type=ticket_type,
                price=price,
                quantity=quantity,
                event_id=event.id,  # Link ticket to the specific event ID
            )

            db.session.add(new_ticket)
            db.session.commit()

            response_dict = new_ticket.serialize()

            response = make_response(
                jsonify(response_dict),
                201,
            )

            return response

    
    
    def get(self):
        response_dict_list = [tickets.serialize() for tickets in Ticket.query.all()]

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
    @jwt_required() #user must be logged in to view orders
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return {'error': 'User not found'}, 404
        else:
            response_dict_list = [orders.serialize() for orders in Order.query.all()]

            response = make_response(
                jsonify(response_dict_list),
                200,
            )

            return response
    

class PostContact(Resource):
    def post(self):
        data = request.get_json()
        full_name = data['full_name']
        email = data['email']
        message = data['message']


        new_contact  = Contact(
           
            full_name=full_name,
            email=email,
            message=message
        )

        db.session.add(new_contact)
        db.session.commit()

        response_dict = new_contact.serialize()

       

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response

class GetEventTickets(Resource):
    def get(self, event_id):
        # Find the event by ID
        event = Event.query.get(event_id)
        if not event:
            return {'error': 'Event not found'}, 404

        # Get tickets associated with the event
        tickets = Ticket.query.filter_by(event_id=event_id).all()
        ticket_data = [ticket.serialize() for ticket in tickets]

        # Return ticket data as JSON response
        return make_response(jsonify(ticket_data), 200)

api.add_resource(GetEventTickets, '/events/<int:event_id>/tickets')

class Postorder(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        current_user = get_jwt_identity()
        user_id = current_user  
        ticket_type = data.get('ticket_type')
        quantity = data.get('quantity')

        # Find the event by name
        event = Event.query.filter_by(event_name=data['event_name']).first()
        if not event:
            return {'error': 'Event not found'}, 404

        # Find the ticket by type
        ticket = Ticket.query.filter_by(event_id=event.id, ticket_type=ticket_type).first()
        if not ticket:
            return {'error': 'Ticket not found for the specified type'}, 404

        # Calculate total price based on the ticket price and quantity
        total_price = int(ticket.price) * int(quantity )  

        if ticket.quantity == 0:
            return {'error': 'Ticket is sold out'}, 400  # Return error if the ticket is sold out
        if int(quantity) == int(0):
            return {'error': 'Quantity cannot be zero'}, 400  # Return error if the quantity is zero
        # Check if there are enough tickets available
        if int(quantity) > int(ticket.quantity): 
            return {'error': 'Not enough tickets available'}, 400

        # Update the quantity of available tickets
        ticket.quantity -= int( quantity )  
            
        # Create a new order
        new_order = Order(
            order_date=datetime.now(),
            total_price=total_price,
            quantity=quantity,
            user_id=user_id,
            event_id=event.id
        )


        db.session.add(new_order)
        db.session.commit()

        response = make_response(jsonify(new_order.serialize()), 201)
        return response
        # return {'message': 'Order created successfully',}, 201
api.add_resource(Postorder, '/order')






api.add_resource(GetTestimonials, '/testimonials')
api.add_resource(BuyTicket, '/tickets')
api.add_resource(GetOrder, '/orders')
api.add_resource(AddEvent, '/events')
api.add_resource(PostContact, '/contacts')





if __name__ == '__main__':
    app.run(port=5555,debug=True)

