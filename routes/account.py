import os
import random

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    current_app
)

from flask_mail import Message

from werkzeug.utils import secure_filename

from models import db
from models.user_model import User

from app import mail

account = Blueprint('account', __name__)

# =========================
# ACCOUNT PAGE
# =========================

@account.route('/account')
def account_page():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    return render_template(
        'account.html',
        user=user,
        active_page="account"
    )


# =========================
# SEND OTP
# =========================

@account.route('/send_otp', methods=['POST'])
def send_otp():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    otp = str(random.randint(100000, 999999))

    session['reset_otp'] = otp

    msg = Message(
        subject="Fitverse AI Password Reset OTP",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email]
    )

    msg.body = f"""
Your Fitverse AI OTP is: {otp}

Enter this OTP to change your password.

If this wasn't you, ignore this email.
"""

    mail.send(msg)

    flash("OTP sent to your registered email 📧")

    return redirect(url_for('account.account_page'))


# =========================
# CHANGE PASSWORD
# =========================

@account.route('/change_password', methods=['POST'])
def change_password():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    entered_otp = request.form['otp']
    new_password = request.form['new_password']

    if entered_otp != session.get('reset_otp'):

        flash("Invalid OTP ❌")

        return redirect(url_for('account.account_page'))

    user.password = new_password

    db.session.commit()

    session.pop('reset_otp', None)

    flash("Password changed successfully 🔥")

    return redirect(url_for('account.account_page'))


# =========================
# UPLOAD PROFILE PHOTO
# =========================

@account.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    if 'profile_pic' not in request.files:

        flash("No file selected ⚠️")
        return redirect(url_for('account.account_page'))

    file = request.files['profile_pic']

    if file.filename == '':

        flash("Please choose an image ⚠️")
        return redirect(url_for('account.account_page'))

    filename = secure_filename(file.filename)

    upload_folder = os.path.join('static', 'uploads')

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, filename)

    file.save(file_path)

    user.profile_pic = filename

    db.session.commit()

    flash("Profile photo uploaded successfully 📸")

    return redirect(url_for('account.account_page'))


# =========================
# UPDATE ACCOUNT
# =========================

@account.route('/update_account', methods=['POST'])
def update_account():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    user.name = request.form['name']
    user.age = request.form['age']
    user.weight = request.form['weight']
    user.height = request.form['height']
    user.goal = request.form['goal']

    db.session.commit()

    flash("Account updated successfully ✨")

    return redirect(url_for('account.account_page'))


# =========================
# DELETE ACCOUNT
# =========================

@account.route('/delete_account', methods=['POST'])
def delete_account():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    db.session.delete(user)

    db.session.commit()

    session.clear()

    flash("Account deleted successfully 🗑️")

    return redirect(url_for('home'))