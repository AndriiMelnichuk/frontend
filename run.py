from app import create_app
from flask_jwt_extended import JWTManager

app = create_app()

# TODO временый код для создания jwt
app.config['JWT_SECRET_KEY']='super'
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)