from flask import Blueprint, jsonify

content_routes = Blueprint('about_subroutes', __name__)

@content_routes.route('/info')
def about_info():
    return jsonify({'message': 'About Info page'})

@content_routes.route('/contact')
def about_contact():
    return jsonify({'message': 'About Contact page'})
