from flask import Flask, session, g, redirect, request
from app.utils import InternetTalker

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Установи секретный ключ для сессий

    # Импорт маршрутов
    from app.routes.group import group
    from app.routes.groups import groups
    from app.routes.main import main
    from app.routes.signin import signin
    from app.routes.signup import signup
    from app.routes.task import task
    from app.routes.calendar import calendar
    from app.routes.google import google

    app.register_blueprint(group, url_prefix='/group')
    app.register_blueprint(groups, url_prefix='/groups')
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(signin, url_prefix='/signin')
    app.register_blueprint(signup, url_prefix='/signup')
    app.register_blueprint(task, url_prefix='/task')
    app.register_blueprint(calendar, url_prefix='/calendar')
    app.register_blueprint(google, url_prefix='/google')

    # Очистка сессии при первом запросе
    @app.before_request
    def clear_session_on_restart():
            if not InternetTalker.isAccesToken():
                if request.endpoint not in ['main.index', 'static', 'signin.signinRoute', 'signin.validateSignIn', 'signup.signupRoute', 'signup.validateSignUp', None, 'google.google_autorize', 'google.google_login_end', 'google.google_login', 'google.validate_id_token_code']:
                    return redirect('/')

    return app
