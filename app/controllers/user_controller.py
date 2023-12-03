from flask import Blueprint, request, jsonify
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
        response = User.query.get(user_id).toDict()
        return jsonify(response)

        # Logic to fetch a single user based on user_id
        return f'User with ID {user_id}'

    @staticmethod
    def create_user(request):
        request_form = request.form.to_dict()

        id = str(uuid.uuid4())
        new_user = User(
                            id             = id,
                            email          = request_form['email'],
                            username       = request_form['username'],
                            password       = request_form['password'],
                            )
        db.session.add(new_user)
        db.session.commit()

        response = User.query.get(id).toDict()
        return jsonify(response)
        
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
        User.query.filter_by(id=user_id).delete()
        db.session.commit()

        return ('User with Id "{}" deleted successfully!').format(user_id)
