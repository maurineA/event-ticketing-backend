# where login logout and signup will be done 
from models import User,bcrypt,db,TokenBlocklist,Company
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity,get_jwt
from flask import Blueprint,jsonify,request,make_response

auth_bp = Blueprint('auth', __name__)

# is staff  == true 


@auth_bp.post('/register')
def signup_for_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    contact = data['contact']
    hashed_password = data['password']

    # check if username and email already exists
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'message': 'Username already exists'}), 404
    
    email_address = User.query.filter_by(email=email).first()
    if email_address:
        return jsonify({'message': 'Email already exists'}), 404
    
    else:
        new_user = User(username=username, email=email, contact=contact, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()

        response = make_response(jsonify(new_user.serialize()), 201)
        return response
    
@auth_bp.post('/signup') 
def signup_for_company():
    data = request.get_json()
    company_name = data['company_name']
    company_email = data['company_email']
    company_contact = data['company_contact']
    hashed_password = data['password']

    # check if company name and email already exists 
    company = Company.query.filter_by(company_name=company_name).first()
    if company:
        return{'error': 'Company already exists'}, 404
    
    email_address = Company.query.filter_by(company_email=company_email).first()
    if email_address:
        return {'error': 'Email already exists'}, 404
    else:

        # password = bcrypt.generate_password_hash(hashed_password.encode('utf-8')).decode('utf-8')
        
        new_company = Company(company_name=company_name, company_email=company_email, company_contact=company_contact, password=hashed_password)
        db.session.add(new_company)
        db.session.commit()

        response = make_response(jsonify(new_company.serialize()), 201)
        return response
    

@auth_bp.post('/companylogin')
def login_company():
    data = request.get_json()
    company_name = data['company_name']
    company = Company.query.filter_by(company_name=company_name).first()
    if not company:
        return {'error': 'Check company name, if you dont have an account please register'}, 401
    
    if not bcrypt.check_password_hash(company.hashed_password, data['password']):
        return {'error': 'Incorrect password'}, 401

    access_token = create_access_token(identity=company.company_name)
    refresh_token = create_refresh_token(identity=company.company_name)

    return jsonify({
        'message': 'Login successful',
        'Token': {
            'access': access_token,
            'refresh': refresh_token,
        }
    }), 200


    
@auth_bp.post('/login')
def login_for_user(): 
    data = request.get_json()
    username = data['username']
    user = User.query.filter_by(username = username).first()
    if not user:
        return {'error': 'check on username,if dont have an account please register'}, 401 
    if not bcrypt.check_password_hash(user.hashed_password,data['password']):
        return{"wrong password try again"},404
    additional_claims = {
        'is_admin': user.is_admin,
        'name':user.username,
    }
    access_token = create_access_token(identity=user.username,additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=user.username)

    return jsonify({
            'message':'login successfull',
            'Token':{
                'access':access_token,
                'refresh':refresh_token,
            }
            
    }),200
    
@auth_bp.get('/whoami')
@jwt_required()
def whoami():
    claims = get_jwt()
    return jsonify({"message":"token","claims":claims})

@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({"access_token":access_token})
    
@auth_bp.get('/logout')
@jwt_required(verify_type=False) #false provides both access and refresh tokens
def logout_user():
    jwt = get_jwt()

    jti = jwt['jti']
    token_type = jwt['type']

    token_blocklist = TokenBlocklist(jti=jti)

    db.session.add(token_blocklist)
    db.session.commit()

    return jsonify({"message":f"{token_type} token revoked successfully"}),200
    


      
