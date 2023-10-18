from flask import Flask, render_template
from flask_session import Session
from dbconnection import db
from base.base import base
from user.user import users
from manager.manager import manager
from admin.admin import admin
from update_pass.update_pass import update_pass
from error.erro import error
import msvcrt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/microservice_'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = '123abc@17686ajhsdaskj'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_COOKIE_SECURE'] = True


db.init_app(app)
Session(app)
app.register_blueprint(base, url_prefix = '/')
app.register_blueprint(users, url_prefix = '/user')
app.register_blueprint(manager, url_prefix = '/manager')
app.register_blueprint(admin, url_prefix = '/admin')
app.register_blueprint(update_pass, url_prefix = '/update_pass')
app.register_blueprint(error, url_prefix = '/error')


if __name__ == '__main__':
    app.run(debug=True)