from models import db,User,Event,Ticket,Contact,Testimonial,TokenBlocklist
from flask_migrate import Migrate
from flask import Flask,jsonify
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity
from auth import auth_bp
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = b'\xb2\xd3B\xb9 \xab\xc0By\x13\x10\x84\xb7M!\x11'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 24 * 60 * 60
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app)
jwt = JWTManager()
jwt.init_app(app)

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
       
# perform other rest routes for  events tickets testimonials and contacts


if __name__ == '__main__':
    app.run(port=5555,debug=True)
