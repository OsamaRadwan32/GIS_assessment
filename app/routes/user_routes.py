from flask import Blueprint, jsonify

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/info')
def about_info():
    return jsonify({'message': 'About Info page'})

@user_routes.route('/contact')
def about_contact():
    return jsonify({'message': 'About Contact page'})
