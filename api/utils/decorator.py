from functools import wraps
from ..models.users import User
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from http import HTTPStatus


#Custom decorator to retrieve user type
def get_user_type(id:int):
    user = User.query.filter_by(id=id).first()
    if user:
        return user.user_type
    else:
        return None
    

#Custom decorator to secure Admin Only Endpoints
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args,**kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            print(claims)
            if get_user_type(claims['sub']) == 'admin':
                return fn(*args,**kwargs)
            return {"message":"Access Denied, Contact an Administrator"}, HTTPStatus.FORBIDDEN
        return decorator
    return wrapper