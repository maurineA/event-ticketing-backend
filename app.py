from models import db,User,Event,Ticket,Contact,Testimonial
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



class User(Resource):
     
    def post(self):

        new_user = User(
            username=request.form['username'],
            email=request.form['email'],
            contact=request.form['contact'],
            password=request.form['password'],
        )

        db.session.add(new_user)
        db.session.commit()

        response_dict = new_user.to_dict()

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response
    

    def get(self, id):

        response_dict = Event.query.filter_by(id=id).first().to_dict()
        
        
        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response
    
class Event(Resource):
     
    def post(self):

        new_event = Event(
            
            event_name=request.form['event_name'],
            start_date=request.form['start_date'],
            end_date=request.form['end_date'],
            event_time=request.form['event_time'],
            venue_name=request.form['venue_name'],
            location=request.form['location'],
            description=request.form['description'],
            event_type=request.form['event_type'],
        )

        db.session.add(new_event)
        db.session.commit()

        response_dict = new_event.to_dict()

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response
    
    
    def get(self, id):

        response_dict = Event.query.filter_by(id=id).first().to_dict()
        
        
        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response

    



api.add_resource(User, 'users/<int:id>')
api.add_resource(Event, 'events/<int:id>')





if __name__ == '__main__':
    app.run(port=5555,debug=True)

