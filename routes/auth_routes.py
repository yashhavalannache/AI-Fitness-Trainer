from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user_model import User
from models import db

auth = Blueprint('auth', __name__)

# =========================
# LOGIN ROUTE
# =========================
@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        # EMAIL CHECK
        if not user:
            flash("Email not registered ❌", "error")
            return redirect(url_for('auth.login'))

        # PASSWORD CHECK
        if user.password != password:
            flash("Invalid password ⚠️", "error")
            return redirect(url_for('auth.login'))

        # SUCCESS LOGIN
        session['user_id'] = user.id
        session['username'] = user.name

        return redirect(url_for('dashboard'))

    return render_template('login.html')


# =========================
# REGISTER ROUTE
# =========================
@auth.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        age = request.form['age']
        height = request.form['height']
        weight = request.form['weight']
        goal = request.form['goal']
        level = request.form['level']
        email = request.form['email']
        password = request.form['password']

        # CHECK DUPLICATE EMAIL
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists ⚠️ Try logging in", "error")
            return redirect(url_for('auth.register'))

        # CREATE USER
        new_user = User(
            name=name,
            age=age,
            height=height,
            weight=weight,
            goal=goal,
            level=level,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully 🚀 Please login", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# =========================
# LOGOUT ROUTE
# =========================
@auth.route('/logout')
def logout():

    session.clear()
    flash("Logged out successfully 👋", "success")
    return redirect(url_for('home'))