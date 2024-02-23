from flask import Flask, render_template, send_from_directory
from routes.user_routes import user_bp
from routes.auth_routes import auth_bp
from routes.mitra_routes import mitra_bp
from routes.admin_routes import admin_bp
from database import app
from config.constants import API_VERSION

app = Flask(__name__)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(mitra_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(auth_bp)

@app.route('/')
def index():
    # return f'Running API Jasa Bantu Versi {API_VERSION}'
    return render_template('index.html')

@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    app.run(debug=True)
    
