from flask import Blueprint, jsonify, request
from ..controllers.authentication_controller import AuthenticationController

authentication_routes = Blueprint('authentication_routes', __name__)

@authentication_routes.route('/login', methods=['POST'])
def login():
    if request.method == 'POST': return AuthenticationController.login(request)
    else: return 'Method is Not Allowed'

@authentication_routes.route('/logout/', methods=['GET'])
def logout():
    return AuthenticationController.logout()