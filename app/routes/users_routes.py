from flask import Blueprint, jsonify, request
from ..controllers.user_controller import UserController

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/', methods=['GET','POST'])
def get_all_or_create():
    if request.method == 'GET': return UserController.get_users()
    if request.method == 'POST': return UserController.create_user(request)
    else: return 'Method is Not Allowed'    

@user_routes.route('/<int:user_id>/', methods=['GET', 'PUT', 'DELETE'])
def get_update_delete(user_id):
    if request.method == 'GET': return UserController.get_user(user_id)
    if request.method == 'PUT': return UserController.update_user(user_id)
    if request.method == 'DELETE': return UserController.delete_user(user_id)
    else: return 'Method is Not Allowed'    
