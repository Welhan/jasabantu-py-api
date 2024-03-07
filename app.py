import os
from flask import Flask, render_template, send_from_directory,jsonify
from routes.user_routes import user_bp
from routes.auth_routes import auth_bp
from routes.mitra_routes import mitra_bp
from routes.admin_routes import admin_bp
from routes.api_routes import api_bp
from database import app

app = Flask(__name__)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(mitra_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)

@app.route('/')
def index():
    return render_template('index.html')
    # return redirect('https://www.contoh.com/link-lain')

@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    app.run(debug=True)
    
