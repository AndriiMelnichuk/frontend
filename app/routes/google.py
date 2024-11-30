from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

from app.utils import Validator, InternetTalker



google = Blueprint('google', __name__)

@google.route('/')
def google_autorize():
    jwt = request.args.get('jwt')
    return render_template('google-entry.html', jwt=jwt)
    
@google.route('/username/<jwt>/')
def google_login_end(jwt):
    username = request.args.get('username')
    error_ans = Validator.getGoogleError(username, jwt)
    if error_ans != '':
        return render_template('google-entry.html', error_message=error_ans, username=username, jwt=jwt)
    return redirect('/')
