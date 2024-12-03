from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
import urllib.parse
from app.utils import Validator, InternetTalker, get_code_url, get_jwt, generate_auth_url



google = Blueprint('google', __name__)

@google.route('/')
def google_autorize():
    jwt = request.args.get('jwt')
    if InternetTalker.isEmailExist(jwt):
        return redirect('/')    
    return render_template('google-entry.html', jwt=jwt)
    
@google.route('/username/<jwt>/')
def google_login_end(jwt):
    username = request.args.get('username')
    error_ans = Validator.getGoogleError(username, jwt)
    if error_ans != '':
        return render_template('google-entry.html', error_message=error_ans, username=username, jwt=jwt)
    return redirect('/')

@google.route('/validate/')
def validate_id_token_code():
    code = request.args.get('code')
    jwt = get_jwt(code)
    
    if InternetTalker.isEmailExist(jwt):
        return redirect('/')    
    return render_template('google-entry.html', jwt=jwt)

@google.route('/validate2/')
def validate_id_token_code2():
    code = request.args.get('code')
    session['access_token'] = code
    return redirect('/')    
    

@google.route('/login/')
def google_login():
    url = get_code_url()
    return redirect(url)

@google.route('/task/add/', methods=['POST'])
def add_task2google_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    if 'access_token' in session.keys():
        InternetTalker.task2calendar(data)
    else:
        return redirect(generate_auth_url())
    return ''

@google.route('/task/isInGoogle/', methods=['POST'])
def is_task_at_google():
    task = request.get_json()
    t = jsonify(False)
    if 'access_token' in session.keys():
        t = jsonify(InternetTalker.is_task_at_google(task))
    return t

@google.route('/task/delete/', methods=['DELETE'])
def delete_task_from_google_route():
    task = request.get_json()
    if 'access_token' in session.keys():
        InternetTalker.delete_task_from_google(task)
    else:
        return redirect(generate_auth_url())
    return ''



