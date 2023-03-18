from api.models.student import Student
from ..utils import db

class Course (db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer(), primary_key=True)
    course_name = db.Column(db.String(45), nullable=False, unique=True)
    teacher = db.Column(db.String(50), nullable=False, unique=True)
    
    
    def __repr__(self):
        return f"<User {self.username}>"


    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

        
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    
    
    
class CourseStudent(db.Model):
    __tablename__ = 'course_student'
    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))

    def __repr__(self):
        return f"< Course Student {self.id}>"
        
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    @classmethod
    def get_student_courses(cls, student_id):
        courses = Course.query.join(CourseStudent).join(Student).filter(Student.id == student_id).all()
        return courses
    
    @classmethod
    def get_students_in_a_course(cls, course_id):
        students = Student.query.join(CourseStudent).join(Course).filter(Course.id == course_id).all()
        return students