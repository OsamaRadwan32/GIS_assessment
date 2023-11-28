from flask import Blueprint, jsonify

about_subroutes = Blueprint('about_subroutes', __name__)

@about_subroutes.route('/info')
def about_info():
    return jsonify({'message': 'About Info page'})

@about_subroutes.route('/contact')
def about_contact():
    return jsonify({'message': 'About Contact page'})
