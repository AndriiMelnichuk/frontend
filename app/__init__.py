from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Импорт маршрутов
    from app.routes.group import group
    from app.routes.groups import groups
    from app.routes.main import main
    from app.routes.signin import signin
    from app.routes.signup import signup
    from app.routes.task import task
    
    app.register_blueprint(group, url_prefix='/group')
    app.register_blueprint(groups, url_prefix='/groups')
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(signin, url_prefix='/signin')
    app.register_blueprint(signup, url_prefix='/signup')
    app.register_blueprint(task, url_prefix='/task')
    
    return app
