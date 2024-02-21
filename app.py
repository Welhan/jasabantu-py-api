from flask import Flask
from routes.user_routes import user_bp
from routes.auth_routes import auth_bp
from routes.mitra_routes import mitra_bp
from routes.admin_routes import admin_bp
from database import app

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(mitra_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
    
