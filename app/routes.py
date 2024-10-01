from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request, exceptions, create_access_token

main = Blueprint('main', __name__)

acces_token = None

@main.route('/signin')
def signin():
    return render_template('sign-in.html')


@main.route('/signup')
def signup():
    return render_template('sign-up.html')


@main.route('/walidate-reg', methods=['POST'])
def walidateReg():
    global acces_token
    error_message = []
    
    name = request.form['username']
    email = request.form['email']
    password = request.form['password']
    password2 = request.form['confirm-password']

    
    # TODO Добавить регистрацию через гугл

    # Проверка данных
    if len(name) < 6:
        error_message.append('Username too short.')
    if len(password) < 6:
        error_message.append('Password too short.')
    if password != password2:
        error_message.append('Password and confirming password not equal.')

    if error_message != []:
        error = ''
        for x in error_message:
            error += ' ' + x
        return render_template('sign-up.html', error_message=error, name=name, email=email, password=password, password2=password2)
    # TODO Добавить отправку на сервер, для проверки существует ли такой пользователь
    # TODO Отправляем запрос на создание токена.
    acces_token = 'some token'
    return redirect('/')


@main.route('/walidate-sign-in', methods=['POST'])
def walidateSignIn():

    # TODO  Добавить отправку сообщения на сервер
    return redirect('/')

@main.route('/')
def index():
    global acces_token
    print(acces_token)
    if acces_token == None:
        return render_template('sign-in-or-up.html')
    return render_template('main.html')

