from flask import Blueprint, jsonify, request
from ..controllers.file_controller import FileController

file_routes = Blueprint('file_routes', __name__)

@file_routes.route('/', methods=['POST'])
def upload_file():
    return FileController.process_request(request)
