from flask import request, render_template, redirect, session
import jwt
from datetime import datetime, timedelta
import secrets
import hashlib
import requests
from functools import wraps
from twilio.base.exceptions import TwilioRestException
import otpauth
from flask import flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from validate_email_address import validate_email
import random

def generate_jwt_token():
    expiration = datetime.utcnow() + timedelta(minutes=5)
    token = jwt.encode({'user_id':'user_id', 'exp': expiration}, '123abc@17686ajhsdaskj' , algorithm='HS256')
    return token, expiration

def generate_otp(phone):
    twilio_account_sid = 'ACd633f573d5e4060a37479baec7778315'
    twilio_auth_token = '83c9e5fe9f64a5f9055b91bd0ad31681'
    twilio_phone_number = '+12562545397'
    twilio_api_url = 'https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json'.format(twilio_account_sid)

    # Generate a secret key for OTP
    otp_secret = random.randint(1000, 9999)
    phone_number = str(phone)  # Convert to string

    #totp = otpauth.TOTP(otp_secret)
    totp = otpauth.TOTP(otp_secret)
    otp_value = str(totp)
    numeric_value = int(hashlib.sha256(otp_value.encode('utf-8')).hexdigest(), 16) % 10000
    formatted_numeric_value = f'{numeric_value:04d}'
    message = f'Your OTP is: {numeric_value}'
    payload = {
            'To': phone_number,
            'From': twilio_phone_number,
            'Body': message,
        }
    payload_bytes = {key: str(value).encode('utf-8') for key, value in payload.items()}
    try:
        auth = (twilio_account_sid, twilio_auth_token)
        response = requests.post(twilio_api_url, data=payload_bytes, auth=auth)

        if response.status_code == 201:
            print("completed.")
        else:
            flash('Failed to send OTP. Please try again.', 'error')

    except TwilioRestException as e:
            flash(f'TwilioRestException: {e}', 'error')
    
    return formatted_numeric_value

def send_email(email):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Use the appropriate port for your SMTP server
    smtp_username = 'techexplorermail@gmail.com'
    smtp_password = 'ioty dppt bmee nmrh'
    recipient_email = email

    try:
        # Create a message
        expiration_time = datetime.utcnow() + timedelta(days=1)
        expiration_timestamp = expiration_time.timestamp()
        reset_link = f'http://127.0.0.1:5000/update_pass/update_password?expires={expiration_timestamp}'
        body = render_template('email_body.html', reset_link=reset_link)
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = email
        msg['Subject'] = 'Welcome'

        msg.attach(MIMEText(body, 'html'))
        # Attach the body to the message

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, recipient_email, msg.as_string())

        flash('Email sent successfully!', 'success')
    except Exception as e:
        print(e)
        flash('Failed to send email. Please try again.', 'error')
    return "hello"


def send_email_for_activation(email):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Use the appropriate port for your SMTP server
    smtp_username = 'priyankpatel.pp12@gmail.com'
    smtp_password = 'nkvt waet ihje uszm'
    recipient_email = 'tapustudio.1608@gmail.com'

    try:
        # Create a message
        otp = random.randint(1000, 9999)
        body = render_template('email_for_otp.html',otp = otp )
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = email
        msg['Subject'] = 'Welcome'

        msg.attach(MIMEText(body, 'html'))
        # Attach the body to the message

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, recipient_email, msg.as_string())
    except Exception as e:
        print(e)
    return otp

def token_required_for_user(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        token = session.get('token')
        if token:
            try:
                decoded_payload = jwt.decode(token, '123abc@17686ajhsdaskj', algorithms=['HS256'])
                expiration_timestamp = decoded_payload['exp']
                expiration_datetime = datetime.utcfromtimestamp(expiration_timestamp)
                current_time = datetime.utcnow()
                
                if current_time > expiration_datetime:
                    flash('Your session has expired. Please log in again.', 'warning')
                    return redirect('/login')
            except jwt.ExpiredSignatureError:
                flash('Your session has expired. Please log in again.', 'warning')
                return redirect('/login')
            except jwt.InvalidTokenError:
                flash('Invalid token. Please log in again.', 'error')
                return redirect('/login')
        return view_func(*args, **kwargs)
    return wrapped_view

def token_required_for_manager(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        token = session.get('token')
        role_id = session.get('role_id')
        if token and role_id == 2:
            try:
                decoded_payload = jwt.decode(token, '123abc@17686ajhsdaskj', algorithms=['HS256'])
                expiration_timestamp = decoded_payload['exp']
                print(type(expiration_timestamp))
                expiration_datetime = datetime.utcfromtimestamp(expiration_timestamp)
                print(type(expiration_datetime))
                current_time = datetime.utcnow()
                print(type(current_time))

                if current_time > expiration_datetime:
                    flash('Your session has expired. Please log in again.', 'warning')
                    return redirect('/login')
            except jwt.ExpiredSignatureError:
                flash('Your session has expired. Please log in again.', 'warning')
                return redirect('/login')
            except jwt.InvalidTokenError:
                flash('Invalid token. Please log in again.', 'error')
                return redirect('/login')
        else:
            flash("You are not a manager!" , 'warning')
            return redirect('/login')
        return view_func(*args, **kwargs)
    return wrapped_view

def token_required_for_admin(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        token = session.get('token')
        role_id = session.get('role_id')
        print(role_id)
        if token and role_id == 3:
            try:
                decoded_payload = jwt.decode(token, '123abc@17686ajhsdaskj', algorithms=['HS256'])
                expiration_timestamp = decoded_payload['exp']
                expiration_datetime = datetime.utcfromtimestamp(expiration_timestamp)
                current_time = datetime.utcnow()

                if current_time > expiration_datetime:
                    flash('Your session has expired. Please log in again.', 'warning')
                    return redirect('/login')
            except jwt.ExpiredSignatureError:
                flash('Your session has expired. Please log in again.', 'warning')
                return redirect('/login')
            except jwt.InvalidTokenError:
                flash('Invalid token. Please log in again.', 'error')
                return redirect('/login')
        else:
            flash("You are not a admin or your are logged out", 'warning')
            return redirect('/')

        return view_func(*args, **kwargs)
    return wrapped_view


def is_valid_email(email):
    return validate_email(email, verify=True)
