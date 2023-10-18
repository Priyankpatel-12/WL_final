from flask import Blueprint, render_template, request, session, redirect, flash
from model import user, auth, role
from dbconnection import db
from common.common import generate_jwt_token, generate_otp, send_email, token_required_for_user, token_required_for_manager,token_required_for_admin, is_valid_email, send_email_for_activation


base = Blueprint('base', __name__, static_folder='asset' , template_folder= 'view')


@base.route('/')
def index():
    return render_template('welcome.html')

@base.route('/login')
def login():
    try:
        return render_template('login.html')
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')

@base.route('/signup')
def signup():
    try:
        return render_template('signup.html')
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')


@base.route('/contact_us')
def contact_us():
    try:
        return render_template('contact_us.html')
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')

@base.route('/add_user' , methods =['POST'])
def add_user():
    try:
        if request.method == 'POST':
            First_name = request.form.get('First_name')
            Last_name = request.form.get('Last_name')
            Email = request.form.get('Email')
            Phone = request.form.get('Phone')
            data = user.query.filter_by(Phone = Phone).first()
            if data == None:
                Role = request.form.get('role')
                if Role == 'user':
                    role_id = 1
                elif Role == 'Manager':
                    role_id = 2
                else :
                    role_id = 3
                Password = request.form.get('Password')
                Confirm_password = request.form.get('Confirm_password')
                if 8 <= len(Password) <= 16:
                    if Password == Confirm_password :
                        otp = send_email_for_activation(Email)
                        flash('Email sent successfully!', 'success')
                        return render_template('otp_for_user.html',role_id = role_id, First_name = First_name, Last_name = Last_name, Email = Email, Phone = Phone, Password = Password,  otp = otp)
                    else:
                        flash("Passwords do not match", 'danger')
                        return redirect('/signup')
                else:
                    flash("Password Must be 8 to 16 char.", 'warning')
                    return redirect('/signup')
            else:
                flash("The mobile number is already in use. Please choose another phone number", 'warning')
                return redirect('/signup')
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')

@base.route('/otp_add_user', methods = ['POST', 'GET'])
def otp_add_user():
    otp = request.form.get('otp')
    digit1 = request.form.get('digit1')
    digit2 = request.form.get('digit2')
    digit3 = request.form.get('digit3')
    digit4 = request.form.get('digit4')
    user_otp = int(f"{digit1}{digit2}{digit3}{digit4}")
    if int(otp) == user_otp:
        role_id = request.form.get('role_id')
        First_name = request.form.get('First_name')
        Last_name = request.form.get('Last_name')
        Email = request.form.get('Email')
        Phone = request.form.get('Phone')
        Password = request.form.get('Password')
        data = user(role_id = role_id, First_name=First_name, Last_name = Last_name, Email = Email, Phone = Phone, Password=Password)
        db.session.add(data)
        db.session.commit()
        flash("You are successfully register!", "success")
        return redirect('/login')
    else:
        flash("Invalid Otp Try again!")
        return redirect('/signup')

@base.route('/check_user', methods=['POST', 'GET'])
def check_user():
    try:
        if request.method == 'POST':
            Phone = request.form.get('Phone')
            Password = request.form.get('Password')
            roles = request.form.get('role')
            rol = role.query.filter_by(role = roles).first()
            data = user.query.filter_by(Phone = Phone).first()
            if data != None and rol.id == data.role_id and data.Phone == Phone and data.Password == Password:
                token, token_exp = generate_jwt_token()
                otp = generate_otp(Phone)
                data = auth(user_id = data.user_id, role_id = data.role_id, token = token, token_exp = token_exp,  otp = otp)
                db.session.add(data)
                db.session.commit()
                return render_template('otp.html', data = data)
            else:
                if data == None:
                    flash("User Not found, First You have to signup!", 'warning')
                elif data.Phone == Phone and data.Password == Password:
                    flash("Select right role!", 'warning')
                else:
                    flash("Phone number and password not match!", 'warning')
                return redirect('/login')
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')
        
@base.route('/check_otp', methods = ['POST'])
def check_otp():
    try:
        id = request.form.get('id')
        digit1 = request.form.get('digit1')
        digit2 = request.form.get('digit2')
        digit3 = request.form.get('digit3')
        digit4 = request.form.get('digit4')
        otp = int(f"{digit1}{digit2}{digit3}{digit4}")
        data = auth.query.filter_by(user_id = id).order_by(auth.id.desc()).first()
        if data.otp == otp :
            if data.role_id == 1:
                session['user_id'] = data.user_id
                session['role_id'] = data.role_id
                session['token'] = data.token
                flash("You are successfully login!", 'success')
                return redirect('/user/user_page')
            elif data.role_id == 2:
                session['user_id'] = data.user_id
                session['role_id'] = data.role_id
                session['token'] = data.token
                flash("You are successfully login!", "success")
                return redirect('/manager/manager_page')
            else :
                session['user_id'] = data.user_id
                session['role_id'] = data.role_id
                session['token'] = data.token
                flash("You are successfully login!", 'success')
                return redirect('/admin/admin_page')
        else:
            return redirect('/login')
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')
    
@base.route('/logout')
def logout():
    try:
        session.pop('token', None)
        flash('You are logged out!', 'info')
        return redirect('/login')
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')
    
