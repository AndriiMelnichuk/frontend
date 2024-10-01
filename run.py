from app import create_app
from flask_jwt_extended import JWTManager

app = create_app()
app.secret_key = 'your_secret_key'

if __name__ == '__main__':
    app.run(debug=True)