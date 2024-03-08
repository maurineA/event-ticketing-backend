from models import db,User,Event,Ticket,Contact,Testimonial, datetime
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

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response
    
    
    # def get(self, id):

    #     response_dict = AddEvents.query.filter_by(id=id).first().to_dict()
        
        
    #     response = make_response(
    #         jsonify(response_dict),
    #         200,
    #     )

    #     return response

    



# api.add_resource(AddUser, '/users/<int:id>')
api.add_resource(AddEvent, '/events')
# api.add_resource(AddEvents, '/events/<int:id>')





if __name__ == '__main__':
    app.run(port=5555,debug=True)

