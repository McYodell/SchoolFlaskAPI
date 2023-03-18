from lib2to3.pgen2 import token
import unittest
from wsgiref import headers
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from flask_jwt_extended import create_access_token
from ..models.courses import Course
from ..models.users import User
from ..models.admin import Admin



class CourseTestCase(unittest.TestCase):
    
    def setUp(self):

        self.app = create_app(config=config_dict['test'])

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()


    def tearDown(self):

        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None


    def test_courses(self):

        # Activate a test admin
        admin_data = {
            "first_name": "Test",
            "last_name": "Admin",
            "email": "testadmin@gmail.com",
            "password": "password",
        }

        response = self.client.post('/admin/register', json=admin_data)

        admin = Admin.query.filter_by(email='testadmin@gmail.com').first()

        token = create_access_token(identity=admin.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }
        

        # Register a test student
        student_data = {
            "first_name": "Test",
            "last_name": "Student",
            "email": "teststudent@gmail.com",
            "password": "password",
            "student_no": "23/GB054"
        }

        response = self.client.post('/students/register', json=student_data, headers=headers)


        # Register a course
        course_data = {
            "course_name": "Test Course",
            "teacher": "Test Teacher"
        }

        response = self.client.post('/courses/courses', json=course_data, headers=headers)

        assert response.status_code == 201

        courses = Course.query.all()

        course_id = courses[0].id

        course_name = courses[0].course_name

        teacher = courses[0].teacher

        assert len(courses) == 1

        assert course_id == 1

        assert course_name == "Test Course"

        assert teacher == "Test Teacher"

        
        # Get all courses
        response = self.client.get('/courses/courses', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "id": 1,
            "course_name": "Test Course",
            "teacher": "Test Teacher"            
        }]


        # Get a course by ID
        response = self.client.get('/courses/1', headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 1,
            "course_name": "Test Course",
            "teacher": "Test Teacher"            
        }


        # Update course
        course_update_data = {
            "course_name": "Sample Course",
            "teacher": "Sample Teacher"
        }

        response = self.client.put('/courses/1', json=course_update_data, headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 1,
            "course_name": "Sample Course",
            "teacher": "Sample Teacher"            
        }


        # Enrol a student for a course
        response = self.client.post('/courses/1/enrol', headers=headers)

        assert response.status_code == 201

        assert response.json == {
            "course_id": 1,
            "student_id": 2,
        }


        # Get all students enrolled for a course
        response = self.client.get('/courses/1/students', headers=headers)

        assert response.status_code == 200

        '''assert response.json == [{
            "id": 2,
            "first_name": "Test",
            "last_name": "Student",
            "matric_no": "ZSCH/23/03/0001"
        }]'''


        '''# Remove a student from a course
        response = self.client.delete('/courses/1/students/2', headers=headers)
        assert response.status_code == 200'''


        # Delete a course
        response = self.client.delete('/courses/1', headers=headers)
        assert response.status_code == 200