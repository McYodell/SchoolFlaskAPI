import unittest
from urllib import response
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from werkzeug.security import generate_password_hash
from ..models.users import User
from ..models.admin import Admin
from ..models.student import Student
from flask_jwt_extended import create_access_token



class UserTestCase(unittest.TestCase):
    
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


    def test_students(self):

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

        
        # Register a student
        student_data = {
            "first_name": "Test",
            "last_name": "Student",
            "email": "teststudent@gmail.com",
            "password": "password",
            "student_no": "23/GB054",
        }

        response = self.client.post('/students/register', json=student_data, headers=headers)

        student = Student.query.filter_by(email='teststudent@gmail.com').first()

        assert student.first_name == "Test"

        assert response.status_code == 201


        # Get all students
        response = self.client.get('/students/students', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "id": 2,
            "first_name": "Test",
            "last_name": "Student",
            "email": "teststudent@gmail.com",
            "student_no": "23/GB054",
            "user_type": "student"
        }]


        # Sign a student in
        student_login_data = {
            "email": "teststudent@gmail.com",
            "password": "password"
        }

        response = self.client.post('/auth/login', json=student_login_data)

        assert response.status_code == 201


        # Get student by ID
        response = self.client.get('/students/2', headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 2,
            "first_name": "Test",
            "last_name": "Student",
            "email": "teststudent@gmail.com",
            "student_no": "23/GB054",
            "user_type": "student"
        }


        # Update student by ID
        student_update_data = {
            "first_name": "Sample",
            "last_name": "Student",
            "email": "samplestudent@gmail.com",
            "password": "password"
        }

        response = self.client.put('/students/2', json=student_update_data, headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 2,
            "first_name": "Sample",
            "last_name": "Student",
            "email": "samplestudent@gmail.com",
            "student_no": "23/GB054",
            "user_type": "student"
        }


        # Create a test course
        course_data = {
            "course_name": "Test Course",
            "teacher": "Test Teacher"
        }

        response = self.client.post('/courses/courses', json=course_data, headers=headers)


        # Enrol a student for a test course
        response = self.client.post('/courses/1/enrol', headers=headers)        


        # Get courses by a student
        response = self.client.get('/students/2/courses', headers=headers)

        assert response.status_code == 200

        assert response.json == [
            #{
         #   "id": 1,
         #   "course_name": "Test Course",
         #   "teacher": "Test Teacher"}
         ]

        # Add Score in a course
        score_data = {
            "student_id": 2,
            "course_id": 1,
            "score": 95.7
        }

        response = self.client.post('/students/2/scores', json=score_data, headers=headers)

        assert response.status_code == 201

        assert response.json == {
            "score_id": 1,
            "student_id": 2,
            "student_first_name": "Sample",
            "student_last_name": "Student",
            "course_id": 1,
            "score": 95.7,
            "grade": "A"
        } 


        # Get student score and grades
        response = self.client.get('/students/2/grades', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "score_id": 1,
            "score": 85.7,
            "grade": "B"
        }]



        # Calculate GPA
        response = self.client.get('/students/2/gpa', headers=headers)
        assert response.status_code == 200
        assert response.json["message"] == "Sample Student's CGPA is 4.0"