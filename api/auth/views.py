import email
from flask import request
from flask_restx import Namespace, Resource, fields
from api.models.admin import Admin
from api.models.student import Student
from api.utils.decorator import admin_required
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, get_jti
from ..utils.blacklist import BLACKLIST


auth_namespace = Namespace('auth', description='Namespace for Authentication')


signup_model = auth_namespace.model(
    'Signup', {
        'first_name': fields.String(required=True, description="First Name"),
        'last_name': fields.String(required=True, description="Last Name"),
        'username': fields.String(required=True, description="A username"),
        'email': fields.String(required=True, description="An email"),
        'password': fields.String(required=True, description="A password")
    }
)

login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True, description="An email"),
        'password': fields.String(required=True, description="A password")
    }
)

user_model = auth_namespace.model(
    'User', {
        'id': fields.Integer(),
        'first_name': fields.String(required=True, description="First Name"),
        'last_name': fields.String(required=True, description="Last Name"),
        'username': fields.String(required=True, description="A username"),
        'email': fields.String(required=True, description="An email"),
        'password_hash': fields.String(required=True, description="A password"),
        'user_type': fields.String(required=True, description="This shows the User Type")
    }
)

'''
@auth_namespace.route('/signup')
class SignUp(Resource):

    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        
         #   Register as a User (Student)
        

        data = request.get_json()
        
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return {"message": "User already exists"}, HTTPStatus.CONFLICT

        new_user = Student(
            first_name = data.get('first_name'),
            last_name = data.get('last_name'),
            username = data.get('username'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password')),
            user_type = 'student'
        )

        new_user.save()

        return new_user, HTTPStatus.CREATED
'''

'''
@auth_namespace.route('/signup/admin')
class AdminSignUp(Resource):

    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    @jwt_required()
    @admin_required()
    def post(self):
        
         #   Register a User (Admin)
        

        data = request.get_json()
        
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return {"message": "User already exists"}, HTTPStatus.CONFLICT

        new_user = Admin(
            first_name = data.get('first_name'),
            last_name = data.get('last_name'),
            username = data.get('username'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password')),
            user_type = 'admin'
        )

        new_user.save()

        return new_user, HTTPStatus.CREATED
'''




@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
            Generate JWT Token
        """

        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return response, HTTPStatus.CREATED


@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
            Generate Refresh Token
        """
        username = get_jwt_identity()

        access_token = create_access_token(identity=username)

        return {'access_token': access_token}, HTTPStatus.OK
    

@auth_namespace.route('/logout')
class Logout(Resource):
    @jwt_required(verify_type=False)
    def post(self):
        """
            Revoke Access/Refresh Token
        """
        token = get_jwt()
        jti = token["jti"]
        token_type = token["type"]
        BLACKLIST.add(jti)
        return {"message": f"{token_type.capitalize()} token successfully revoked"}, HTTPStatus.OK