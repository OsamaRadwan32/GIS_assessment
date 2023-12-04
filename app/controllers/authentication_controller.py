from flask import Flask, request, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash

from .. import app
from .user_controller import UserController

# app.secret_key = 'your_secret_key_here'  # Used to encrypt session data, replace with your secret key

class AuthenticationController:

    @staticmethod
    def login(request):

        email = request.form['email']
        password = request.form['password']

        user = UserController.find_user_by_email(email)

        if user is None:
            return jsonify({'message': 'Invalid username'})

        is_password_correct = check_password_hash(user['password'], password)

        if is_password_correct:
            return user
        else:
            return jsonify({'message': 'Invalid password'})


    @staticmethod
    def logout():
        session.pop('logged_in', None)
        session.pop('email', None)
        return true
