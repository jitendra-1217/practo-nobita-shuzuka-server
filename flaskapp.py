import os
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory
from doctor_api.app import doctor_api_bp
from patient_api.app import patient_api_bp

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

app.register_blueprint(doctor_api_bp, url_prefix='/doctor-api')
app.register_blueprint(patient_api_bp, url_prefix='/patient-api')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@app.route("/test")
def test():
    return "<strong>It's Alive!</strong>"

if __name__ == '__main__':
    app.run(app.config['IP'], app.config['PORT'], debug=True)
