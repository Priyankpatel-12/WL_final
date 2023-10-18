from flask import Blueprint, render_template, request, session, redirect, flash
from common.common import send_email
from dbconnection import db
from datetime import datetime
from model import user, auth, role

update_pass = Blueprint('update_pass', __name__, static_folder='asset' , template_folder= 'view')


@update_pass.route('/email_pass')
def email_pass():
    try:
        return render_template('email_for_resetpass.html')
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')

@update_pass.route('/pass_reset', methods = ['POST'])
def pass_reset():
    try:
        email = request.form.get('email')
        session['pass_email'] = email
        data = user.query.filter_by(Email = email).first()
        if data != None:
            send_email(email)
            return render_template('success_email.html')
        else:
            flash("Plz Enter Registred Mail Id.")
        return redirect('/update_pss/email_pass')
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')

@update_pass.route('/update_password')
def update_password():
    try:
        expiration_timestamp = request.args.get('expires')
        if expiration_timestamp:
            expiration_time = datetime.utcfromtimestamp(float(expiration_timestamp))
            current_time = datetime.utcnow()
            if current_time <= expiration_time:
                return render_template('reset_pass.html')
            else:
                return render_template('exp_email.html')
    except Exception as e:
        print(str(e))
        flash("Some Error From Serverside!",'warning')
    return redirect('/')

@update_pass.route('/check_update_password', methods = ['POST', 'GET'])
def check_update_password():
    try:
        password = request.form.get('Password')
        confirm_password = request.form.get('Confirm_password')
        email = session.get('pass_email')
        data = user.query.filter_by(Email = email).first()

        if password == confirm_password :
            data.Password = password
            db.session.add(data)
            db.session.commit()
            flash("Your Password updated.", 'success')
            return redirect('/login')
        else :
            flash("Password must be same.")
        return redirect('/update_pass/check_update_password')
    except Exception as e:
        flash("Some Error From Serverside!",'warning')
        return redirect('/')