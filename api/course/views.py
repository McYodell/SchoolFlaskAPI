
from flask_restx import Namespace, Resource, fields
from ..models.courses import Course, CourseStudent
from ..models.users import User
from ..models.student import Student
from ..models.scores import Score
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import db
from ..utils.decorator import admin_required



course_namespace = Namespace('courses', description='Namespace for Courses')

course_model = course_namespace.model(
    'Course', {
        'id': fields.Integer(description='Course Id'),
        'course_name': fields.String(description='Name of Course', required=True),
        'teacher': fields.String(description='Course Teacher'),
    }
)


course_student_model = course_namespace.model(
    'CourseStudent', {
        'student_id': fields.Integer(description='Student Id', required=True),
        'course_id': fields.Integer(description='Course Id', required=True)
    }
)


@course_namespace.route('/courses')
class CourseGetCreate(Resource):
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Get all Courses'
    )
    @jwt_required()
    def get(self):
        """
            Get All Courses
        """
        courses = Course.query.all()

        return courses, HTTPStatus.OK



    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Create a Course'
    )
    @jwt_required()
    @admin_required()
    def post(self):
        
        """
            Create a Course
        """

        data = course_namespace.payload
        course = Course.query.filter_by(course_name=data['course_name']).first()
        if course:
            return {"message": "Course Already Exists"}, HTTPStatus.CONFLICT
            

        new_course = Course(
            course_name = data['course_name'],
            teacher = data['teacher']
        )

        new_course.save()

        course_display = {}
        course_display['id'] = new_course.id
        course_display['course_name'] = new_course.course_name
        course_display['teacher'] = new_course.teacher
        
        return course_display, HTTPStatus.CREATED





@course_namespace.route('/<int:course_id>')
class CourseGetUpdateDelete(Resource):

    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Get a Course by ID',
    )
    @jwt_required()
    def get(self, course_id):
        """
            Get a Course by ID
        """        
        course = Course.get_by_id(course_id)

        return course, HTTPStatus.OK



    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Update a Course by ID'
    )
    @jwt_required()
    @admin_required()
    def put(self, course_id):
         
        '''
        Update a Course by id
        '''
        course_to_update = Course.get_by_id(course_id)
        
        data = course_namespace.payload
        
        course_to_update.course_name = data ["course_name"]
        course_to_update.teacher = data ["teacher"]
        

        db.session.commit()
        
        return course_to_update, HTTPStatus.OK
        
        
         
    @course_namespace.doc(
        description='Delete a Course by ID'
    )  
    @jwt_required()
    @admin_required()
    def delete(self, course_id):
        
        '''
        Delete a Course by id
        '''
        course_to_delete = Course.get_by_id(course_id)
        
        course_to_delete.delete()
        
        return {"message":"Course Successfully Deleted"}, HTTPStatus.OK



@course_namespace.route('/<int:course_id>/students')
class GetAllCourseStudents(Resource):

    @course_namespace.doc(
        description = "Get all Students Enrolled for a Specific Course",
        params = {
            'course_id': "Course ID"
        }
    )
    @jwt_required()
    @admin_required()
    def get(self, course_id):
        """
            Get all Students Enrolled for a Specific Course
        """
        students = CourseStudent.get_students_in_a_course(course_id)
        
        display = []

        for student in students:
            student_display = {}
            student_display['id'] = student.id
            student_display['first_name'] = student.first_name
            student_display['last_name'] = student.last_name
            student_display['student_no'] = student.student_no

            display.append(student_display)

        return display, HTTPStatus.OK


    
    
@course_namespace.route('/<int:course_id>/enrol')
class EnrolStudents(Resource):
    @course_namespace.expect(course_student_model)
    @course_namespace.marshal_with(course_student_model)
    @course_namespace.doc(
        description='Enrol students for a course',
        params = {
            'course_id': "The Course's ID"
        }
    )
    @jwt_required()
    @admin_required()
    def post(self, course_id):
        """
            Enrol Students for a Course
        """
        data = course_namespace.payload

        student_to_enrol =  User(
            course_id = course_id,
            student_id = data['student_id']
        )

        student_to_enrol.save()

        return student_to_enrol, HTTPStatus.CREATED
