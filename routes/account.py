import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.utils import secure_filename

from models import db
from models.user_model import User

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
# UPLOAD PROFILE PHOTO
# =========================

@account.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    # CHECK FILE
    if 'profile_pic' not in request.files:

        flash("No file selected ⚠️")
        return redirect(url_for('account.account_page'))

    file = request.files['profile_pic']

    if file.filename == '':

        flash("Please choose an image ⚠️")
        return redirect(url_for('account.account_page'))

    # SAFE FILE NAME
    filename = secure_filename(file.filename)

    # CREATE UPLOAD FOLDER
    upload_folder = os.path.join('static', 'uploads')

    os.makedirs(upload_folder, exist_ok=True)

    # SAVE FILE
    file_path = os.path.join(upload_folder, filename)

    file.save(file_path)

    # SAVE INTO DATABASE
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