from flask import Blueprint, render_template, request, session, redirect, flash
from common.common import generate_jwt_token, generate_otp, send_email, token_required_for_user, token_required_for_manager,token_required_for_admin, is_valid_email
from dbconnection import db
from model import user, auth, role

users = Blueprint('users', __name__, static_folder='asset' , template_folder= 'view')


@users.route('/user_page')
@token_required_for_user
def user_page():
    try:
        return render_template("user.html")
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')

@users.route('/update_user', methods = ['POST', 'GET'])
@token_required_for_user
def update_user():
    try:
        id = session.get('user_id')
        data = user.query.filter_by(user_id = id).first()
        return render_template('update_user.html', data = data)
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')

@users.route('/update_details', methods = ['POST', 'GET'])
@token_required_for_user
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
        return redirect('/user/user_page')
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')
