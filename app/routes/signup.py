from flask import Blueprint, render_template, request, redirect

from app.utils import Validator 

signup = Blueprint('signup', __name__)

@signup.route('/')
def signupRoute():
    return render_template('sign-up.html')

@signup.route('/validate', methods=['POST'])
def validateSignUp():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    password2 = request.form['confirm-password']

    error_ans = Validator.getSignUpErrorMessage(username, email, password, password2)
    if error_ans != '':
        return render_template('sign-up.html', error_message=error_ans, name=username, email=email, password=password, password2=password2)
    return redirect('/')


