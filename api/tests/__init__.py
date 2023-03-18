

'''




    
   
        
    student_data = {
        "first_name": "Test",
        "last_name": "Student",
        "email": "teststudent@gmail.com",
        "password": "password",
        "student_no": "23/GB054"
        }
    
    
    course_data = {
        "name": "Test Course",
        "teacher": "Test Teacher"
        }
    
    
    def test_admin_signup(self):

        admin_data = {
            "first_name": "Test",
            "last_name": "Admin",
            "email": "testadmin@gmail.com",
            "password": "password"
        }
        
        admin = Admin.query.filter_by(email='testadmin@gmail.com').first()

        token = create_access_token(identity=admin.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.post('/admin/register', json=admin_data, headers=headers)






'''





'''








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
        
        
        
        
    def test_get_all_courses(self):
        
        token = create_access_token(identity='testuser')
        
        headers = {
            "Authorization" : f"Bearer {token}"
        }
        response = self.client.get('courses/courses', headers=headers)
        
        assert response.status_code == 200
        
        assert response.json == []
        
    
    def test_create_course(self):
        data = {
            "course_name": "Science",
            "teacher": "Olusola"
            }
        
        token = create_access_token(identity='testuser')
        
        headers = {
            "Authorization" : f"Bearer {token}"
        }
        response = self.client.post('/courses/courses', json=data, headers=headers)
        
        assert response.status_code == 201
        
       
        courses = Course.query.all()
        
        course_id = courses[0].id
        
        course_name = courses[0].course_name
        
        teacher = courses[0].teacher
        
        assert course_id == 1
        
        assert len(courses) == 1
        
        assert course_name == "Science"
        
        assert teacher == "Olusola"
        
        
        
    def test_get_course_by_id(self):
        
       
        token = create_access_token(identity='testuser')
    
        headers = {
            "Authorization" : f"Bearer {token}"
        }
        
        response = self.client.get('/course/courses/<int:course_id>', headers=headers)
        
        assert response.status_code == 404





'''











'''



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
        
        
    def test_user_registration(self):
        
        data = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "password",
            "is_admin": "True"
        }
        
        response = self.client.post('/auth/signup', json=data)
        
        user = User.query.filter_by(email='testuser@gmail.com').first()
        
        assert user.first_name == "Test"
        
        assert user.username == "testuser"
        
        assert response.status_code == 201
        
    
    def test_user_login(self):
        data = {
            "email": "testuser@gmail.com",
            "password": "password"
        }
        
        response = self.client.post('/auth/login', json=data)
        
        assert response.status_code == 200








'''