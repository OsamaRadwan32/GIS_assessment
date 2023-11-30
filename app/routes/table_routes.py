from flask import Blueprint, jsonify

table_routes = Blueprint('table_routes', __name__)

@table_routes.route('/info')
def about_info():
    return jsonify({'message': 'About Info page'})

@table_routes.route('/contact')
def about_contact():
    return jsonify({'message': 'About Contact page'})
