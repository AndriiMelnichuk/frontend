from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

from app.utils import Validator, InternetTalker
from app.models import Group

signin = Blueprint('signin', __name__)

@signin.route('/')
def signinRoute():
    return render_template('sign-in.html')


@signin.route('/validate', methods=['POST'])
def validateSignIn():
    username = request.form['username']
    password = request.form['password']

    error_ans = Validator.getSignInErrorMessage(username, password)
    if error_ans != '':
        return render_template('sign-in.html', error_message=error_ans, username=username, password=password)
    return redirect('/')




