from flask import Flask
from routes.user_routes import user_bp
from routes.register_routes import register_bp
from database import app

app.register_blueprint(user_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
    app.register_blueprint(register_bp, url_prefix='/api')
