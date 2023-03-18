
from flask_restx import Namespace, Resource, fields
from ..models.courses import Course, CourseStudent
from ..models.users import User
from ..models.student import Student
from ..models.scores import Score
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..utils import db
from ..utils.decorator import admin_required, get_user_type
from werkzeug.security import generate_password_hash
from ..utils.score_conversion import get_grade, grade_to_gpa


student_namespace = Namespace('students', description='Namespace for Students')

student_signup_model = student_namespace.model(
    'StudentSignup', {
        'first_name': fields.String(required=True, description="First Name"),
        'last_name': fields.String(required=True, description="Last Name"),
        'email': fields.String(required=True, description="Email"),
        'password': fields.String(required=True, description="Password"),
        'student_no': fields.String(required=True, description="Student Number")
    }
)


student_model = student_namespace.model(
    'Student', {
        'id': fields.Integer(description="Student's User ID"),
        'first_name': fields.String(required=True, description="First Name"),
        'last_name': fields.String(required=True, description="Last Name"),
        'email': fields.String(required=True, description="Email"),
        'student_no': fields.String(required=True, description="Student Number"),    
        'user_type': fields.String(required=True, description="Type of User")
    }
)

student_course_model = student_namespace.model(
    'StudentCourse', {
        'student_id': fields.Integer(description="Student's User ID"),
        'course_id': fields.Integer(description="Course's ID")
    }
)

student_score_model = student_namespace.model(
    'Score', {
        'id': fields.Integer(description="Score ID"),
        'course_id': fields.Integer(required=True, description="Course ID"),
        'score': fields.Float(required=True, description="Score in course"),
        'grade': fields.String(required=True, description="Grade in course") 
    }
)


def adminOrStudent(student_id:int) -> bool:
    claims = get_jwt()
    current_user_id = get_jwt_identity()
    if (get_user_type(claims['sub']) == 'admin') or (current_user_id == student_id):
        return True
    else:
        return False




@student_namespace.route('/register')
class RegisterStudent(Resource):

    @student_namespace.expect(student_signup_model)
    @student_namespace.doc(
        description = "Register a Student"
    )
    @admin_required()
    def post(self):
        """
            Register a Student
        """        
        data = student_namespace.payload

        # Check if student has already been registered
        student = Student.query.filter_by(email=data['email']).first()
        if student:
            return {"message": "Student already registered"}, HTTPStatus.CONFLICT

    
        new_student = Student(
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            password_hash = generate_password_hash(data['password']),
            student_no = data['student_no'],
            user_type = 'student'
        )

        new_student.save()

        student_display = {}
        
        student_display['id'] = new_student.id
        student_display['first_name'] = new_student.first_name
        student_display['last_name'] = new_student.last_name
        student_display['email'] = new_student.email
        student_display['student_no'] = new_student.student_no
        student_display['user_type'] = new_student.user_type

        return student_display, HTTPStatus.CREATED
    



@student_namespace.route('/students')
class GetAllStudents(Resource):

    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description = "Get All Students"
    )
    
    @admin_required()
    def get(self):
        """
            Get All Students
        """
        students = Student.query.all()

        return students, HTTPStatus.OK
    



@student_namespace.route('/<int:student_id>')
class GetUpdateDeleteStudents(Resource):
    
    @student_namespace.doc(
        description = "Get Student by ID",
        params = {
            'student_id': "Student ID"
        }
    )
    @jwt_required()
    def get(self, student_id):
        """
            Get Student by ID
        """
        if adminOrStudent(student_id):
            
            student = Student.get_by_id(student_id)

            student_display = {}  
            student_display['id'] = student.id
            student_display['first_name'] = student.first_name
            student_display['last_name'] = student.last_name
            student_display['email'] = student.email
            student_display['student_no'] = student.student_no
            student_display['user_type'] = student.user_type

            return student_display, HTTPStatus.OK
        
        else:
            return {"message": "Access Unauthorised"}, HTTPStatus.FORBIDDEN

    
    
    @student_namespace.expect(student_signup_model)
    @student_namespace.doc(
        description = "Update Student by ID",
        params = {
            'student_id': "Student ID"
        }
    )
    @jwt_required()
    def put(self, student_id):
        """
            Update Student by ID
        """
        if adminOrStudent(student_id):
            student = Student.get_by_id(student_id)
            
            data = student_namespace.payload

            student.first_name = data['first_name']
            student.last_name = data['last_name']
            student.email = data['email']
            student.password_hash = generate_password_hash(data['password'])

            student.update()

            student_display = {}  
            student_display['id'] = student.id
            student_display['first_name'] = student.first_name
            student_display['last_name'] = student.last_name
            student_display['email'] = student.email
            student_display['student_no'] = student.student_no
            student_display['user_type'] = student.user_type

            return student_display, HTTPStatus.OK

        else:
            return {"message": "Access Unauthorised"}, HTTPStatus.FORBIDDEN
    
    

    @student_namespace.doc(
        description = 'Delete Student by ID',
        params = {
            'student_id': "Student ID"
        }
    )
    @admin_required()
    def delete(self, student_id):
        """
            Delete Student by ID
        """
        student_to_delete = Student.get_by_id(student_id)

        student_to_delete.delete()

        return {"message": "Student Deleted Successfully"}, HTTPStatus.OK
    


    
    
@student_namespace.route('/<int:student_id>/courses')
class GetStudentCourse(Resource):

    @student_namespace.doc(
        description = "Get all Courses Taken by a Specific Student",
        params = {
            'student_id': "Student ID"
        }
    )
    @jwt_required()
    def get(self, student_id):
        """
            Get all Courses Taken by a Specific Student
        """
        if adminOrStudent(student_id):
            
            courses = CourseStudent.get_student_courses(student_id)
            
            display = []

            for course in courses:
                course_display = {}
                course_display['id'] = course.id
                course_display['name'] = course.name
                course_display['teacher'] = course.teacher

                display.append(course_display)
            
            return courses, HTTPStatus.OK
    
        else:
            return {"message": "Access Unauthorised"}, HTTPStatus.FORBIDDEN



@student_namespace.route('/<int:student_id>/scores')
class AddStudentScore(Resource):
    
    @student_namespace.expect(student_score_model)
    @student_namespace.doc(
            description = "Add Student Score in a Course",
            params = {
                'student_id': "Student ID"
            }
        )
    @jwt_required()
    @admin_required()
    def post(self, student_id):
        """
            Add Student Score in a Course
        """
        data = student_namespace.payload

        student = Student.get_by_id(student_id)
        course = Course.get_by_id(id=data['course_id'])
        
        # Check if the student whose score is to be added is registered for the course.
        course_student = CourseStudent.query.filter_by(student_id=student_id, course_id=course.id).first()
        if not course_student:
            return {"message": f"{student.first_name} {student.last_name} is not registered for {course.course_name}"}, HTTPStatus.NOT_FOUND
        
        # Add the score
        new_score = Score(
            student_id = student_id,
            course_id = data['course_id'],
            score = data['score'],
            grade = get_grade(data['score'])
        )

        new_score.save()

        score_display = {}
        score_display['student_id'] = new_score.student_id
        score_display['student_first_name'] = student.first_name
        score_display['student_last_name'] = student.last_name
        score_display['course_id'] = new_score.course_id
        score_display['score'] = new_score.score
        score_display['grade'] = new_score.grade

        return score_display, HTTPStatus.CREATED



@student_namespace.route('/<int:student_id>/scores')
class GetScoreAndGrade(Resource):

    @student_namespace.doc(
        description = "Get Student Score and Grade",
        params = {
            'student_id': "Student ID"
        }
    )
    @jwt_required()
    def get(self, student_id):
        """
            Get Student Score and Grade
        """
        if adminOrStudent(student_id):

            student = Student.query.filter_by(id=student_id).first()
            if not student:
                return {"message": "Student Not Found"}, HTTPStatus.NOT_FOUND
                  
            courses = CourseStudent.get_student_courses(student_id)
            display = []

            for course in courses:
                score_display = {}
                course_score = Score.query.filter_by(
                        student_id=student_id, course_id=course.id
                    ).first()
                score_display['course_name'] = course.name

                if course_score:
                    score_display['score_id'] = course_score.id
                    score_display['score'] = course_score.score
                    score_display['grade'] = course_score.grade
                else:
                    score_display['score'] = None
                    score_display['grade'] = None
                
                display.append(score_display)
            
            return display, HTTPStatus.OK
        
        else:
            return {"message": "Access Unauthorised"}, HTTPStatus.FORBIDDEN
        


@student_namespace.route('/<int:student_id>/gpa')
class GetCGPA(Resource):

    @student_namespace.doc(
        description = "Calculate Student GPA",
        params = {
            'student_id': "Student ID"
        }
    )
    @jwt_required()
    def get(self, student_id):
        """
            Calculate Student GPA
        """
        if adminOrStudent(student_id):

            student = Student.get_by_id(student_id)
            
            courses = CourseStudent.get_student_courses(student_id)
            total_gpa = 0
            
            for course in courses:
                score = Score.query.filter_by(student_id=student_id, course_id=course.id).first()
                
                if score:
                    grade = score.grade
                    gpa = grade_to_gpa(grade)
                    total_gpa += gpa
                
            cgpa = total_gpa / len(courses)
            round_cgpa = round(cgpa, 2)

            return {"message": f"{student.first_name} {student.last_name}'s CGPA is {round_cgpa}"}, HTTPStatus.OK
    
        else:
            return {"message": "Access Unauthorised"}, HTTPStatus.FORBIDDEN