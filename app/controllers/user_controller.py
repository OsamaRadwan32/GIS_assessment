from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from .. import db
from ..models.users_models import User

user_bp = Blueprint('user_bp', __name__)

class UserController:

    @staticmethod
    def get_users():
        users = User.query.all()
        response = []
        for user in users: response.append(user.toDict())
        return jsonify(response)

    @staticmethod
    def get_user(user_id):
        response = User.query.get(user_id)
        if response is not None:
            return response.toDict()
        return jsonify({'message': 'User not found'}), 404

    @staticmethod
    def find_user_by_email(email):
        response = User.query.filter_by(email=email).first()
        return response

    @staticmethod
    def create_user(request):
        request_form = request.form.to_dict()

        user = UserController.find_user_by_email(request_form['email'])

        if user is not None:
            return jsonify({'message': 'User already exists'})

        # Encrypting the password
        hashed_password = generate_password_hash(request_form['password'])

        new_user = User(
                        email          = request_form['email'],
                        username       = request_form['username'],
                        password       = hashed_password,
                        )
        db.session.add(new_user)
        db.session.commit()

        response = User.query.filter_by(email=request_form['email']).first()
        return response.toDict()
        
    @staticmethod
    def update_user(user_id):
            request_form = request.form.to_dict()
            user = User.query.get(user_id)

            user.email        = request_form['email']
            user.username     = request_form['username']
            user.password     = request_form['password']
            db.session.commit()

            response = Account.query.get(user_id).toDict()
            return jsonify(response)

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user is not None:
            User.query.filter_by(id=user_id).delete()
            db.session.commit()
            return jsonify({'message': f'User with id {user_id} deleted successfully!'})
        return jsonify({'message': 'Failed to delete record or not found!'})
