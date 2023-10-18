from flask import Blueprint, render_template, request, session, redirect, flash
from model import user, auth, role
from dbconnection import db
from common.common import generate_jwt_token, generate_otp, send_email, token_required_for_admin, is_valid_email
from validate_email_address import validate_email

admin = Blueprint('admin', __name__, static_folder='asset' , template_folder= 'view')

@admin.route('/admin_page')
@token_required_for_admin
def admin_page():
    try:
        return render_template("admin.html")
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')

@admin.route('/admin_user')
@token_required_for_admin
def admin_user():
    try:
        user_data = user.query.filter_by(role_id = 1).all()
        return render_template('admin_user.html', user = user_data)
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')

@admin.route('update_user_by_admin')
@token_required_for_admin
def update_user_by_admin():
    try:
        id = request.args.get('user_id')
        data = user.query.filter_by(user_id = id).first()
        return render_template('update_user_by_admin.html', data = data)
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')

@admin.route('/update_userdetails_by_admin', methods = ['POST', 'GET'])
@token_required_for_admin
def update_userdetails_by_admin():
    try:
        id = request.form.get('user_id')
        data = user.query.filter_by(user_id = id).first()
        data.First_name = request.form.get('First_name')
        data.Last_name = request.form.get('Last_name')
        data.Email = request.form.get('Email')
        data.Phone = request.form.get('Phone')
        db.session.add(data)
        db.session.commit()
        return redirect('/admin/admin_user')
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')

@admin.route('/delete_user')
@token_required_for_admin
def delete_user():
      try:
        id = request.args.get('user_id')
        data = user.query.get(id)
        if data:
            db.session.delete(data)
            db.session.commit()
        return redirect('/admin/admin_user')
      except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')

@admin.route('/admin_manager')
@token_required_for_admin
def admin_manager():
    try:
        user_data = user.query.filter_by(role_id = 2).all()
        return render_template('admin_manager.html', user = user_data)
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')

@admin.route('/update_manager_by_admin')
@token_required_for_admin
def update_manager_by_admin():
    try:
        id = request.args.get('user_id')
        data = user.query.filter_by(user_id = id).first()
        return render_template('update_manager_by_admin.html', data = data)
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')

@admin.route('/update_managerdetails_by_admin', methods = ['POST', 'GET'])
@token_required_for_admin
def update_managerdetails_by_admin():
    try:
        id = request.form.get('user_id')
        data = user.query.filter_by(user_id = id).first()
        data.First_name = request.form.get('First_name')
        data.Last_name = request.form.get('Last_name')
        data.Email = request.form.get('Email')
        data.Phone = request.form.get('Phone')
        db.session.add(data)
        db.session.commit()
        return redirect('/admin/admin_manager')
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')

@admin.route('/delete_manager')
@token_required_for_admin
def delete_manager():
    try:
      id = request.args.get('user_id')
      data = user.query.get(id)
      if data:
        db.session.delete(data)
        db.session.commit()
      return redirect('/admin/admin_manager')
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')
