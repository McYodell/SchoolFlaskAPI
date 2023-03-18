from flask_restx import Namespace, Resource, fields
from ..models.admin import Admin
from ..utils.decorator import admin_required
from werkzeug.security import generate_password_hash
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity


admin_namespace = Namespace('admin', description='Namespace for Admin')


admin_signup_model = admin_namespace.model(
    'AdminSignup', {
        'first_name': fields.String(required=True, description="Admin's First Name"),
        'last_name': fields.String(required=True, description="Admin's Last Name"),
        'email': fields.String(required=True, description="Admin's Email"),
        'password': fields.String(required=True, description="Admin's Password")
    }
)

admin_model = admin_namespace.model(
    'Admin', {
        'id': fields.Integer(description="Admin User ID"),
        'first_name': fields.String(required=True, description="First Name"),
        'last_name': fields.String(required=True, description="Last Name"),
        'email': fields.String(required=True, description="Email"),
        'user_type': fields.String(required=True, description="User Type")
    }
)

@admin_namespace.route('')
class GetAllAdmins(Resource):

    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(
        description="Get All Admins"
    )
    @admin_required()
    def get(self):
        """
            Get All Admins
        """
        admins = Admin.query.all()

        return admins, HTTPStatus.OK



@admin_namespace.route('/register')

class RegisterAdmin(Resource):
# After the first admin is created, the decorator @admin_required() will be imposed on this endpoint /
# to secure it
    @admin_namespace.expect(admin_signup_model)
    @admin_namespace.doc(
        description = "Register an Admin"
    )
    def post(self):
        """
            Register an Admin
        """        
        data = admin_namespace.payload

        # Check if the admin account already exists
        admin = Admin.query.filter_by(email=data['email']).first()
        if admin:
            return {"message": "Admin Already Exist"}, HTTPStatus.CONFLICT

        new_admin = Admin(
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            password_hash = generate_password_hash(data['password']),
            user_type = 'admin'
        )

        new_admin.save()

        admin_resp = {}
        admin_resp['id'] = new_admin.id
        admin_resp['first_name'] = new_admin.first_name
        admin_resp['last_name'] = new_admin.last_name
        admin_resp['email'] = new_admin.email
        admin_resp['user_type'] = new_admin.user_type

        return admin_resp, HTTPStatus.CREATED



@admin_namespace.route('/<int:admin_id>')
class GetAdmin(Resource):
    
    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(
        description = "Get Admin by ID ",
        params = {
            'admin_id': "Admin ID"
        }
    )
    @admin_required()
    def get(self, admin_id):
        """
            Get Admin by ID
        """
        admin = Admin.get_by_id(admin_id)
        
        return admin, HTTPStatus.OK