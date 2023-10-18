from flask import Blueprint, render_template, request, session, redirect, flash
from common.common import generate_jwt_token, generate_otp, send_email, token_required_for_user, token_required_for_manager,token_required_for_admin, is_valid_email
from dbconnection import db
from model import user, auth, role

manager = Blueprint('manager', __name__, static_folder='asset' , template_folder= 'view')


@manager.route('/manager_page')
@token_required_for_manager
def manager_page():
    try:
        return render_template("manager.html")
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')

@manager.route('/update_manager', methods = ['POST', 'GET'])
@token_required_for_manager
def update_user():
    try:
        id = session.get('user_id')
        data = user.query.filter_by(user_id = id).first()
        return render_template('update_user.html', data = data)
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')

@manager.route('/update_details', methods = ['POST', 'GET'])
@token_required_for_manager
def update_details():
    try:
        id = session.get('user_id')
        data = user.query.filter_by(user_id = id).first()
        data.First_name = request.form.get('First_name')
        data.Last_name = request.form.get('Last_name')
        data.Email = request.form.get('Email')
        data.Phone = request.form.get('Phone')
        db.session.add(data)
        db.session.commit()
        return redirect('/login')
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')