from flask import Flask
from .config.config import config_dict
from .utils import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .auth.views import auth_namespace
from flask_restx import Api
from .course.views import course_namespace
from .students.views import student_namespace
from .admin.views import admin_namespace
from .models.courses import Course
from .models.users import User


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)
    
    authorizations = {
        "Bearer Auth" : {
            "type": "apiKey",
            "in" : "header",
            "name" : "Authorization",
            "description" : "Add a JWT token to the header with ** Bearer &lt;JWT&gt; token to authorize**"
        }
    }

    api = Api(app,
              title = 'Student Management System API',
              description='A Student Management System Rest API Service',
              authorizations=authorizations,
              security='Bearer Auth'
              ) 

    api.add_namespace(course_namespace, path='/courses')
    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(student_namespace, path='/students')
    api.add_namespace(admin_namespace, path='/admin')
    
    
    
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Course': Course
        }

  
    return app