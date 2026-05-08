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

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))

        else:
            flash("Invalid credentials ⚠️ Please try again", "error")
            return redirect(url_for('auth.login'))

    return render_template('login.html')


# =========================
# REGISTER ROUTE (FIXED)
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

        # ✅ CHECK DUPLICATE EMAIL
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists ⚠️ Try logging in", "error")
            return redirect(url_for('auth.register'))

        # ✅ CREATE USER
        user = User(
            name=name,
            age=age,
            height=height,
            weight=weight,
            goal=goal,
            level=level,
            email=email,
            password=password
        )

        db.session.add(user)
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
    return redirect(url_for('home'))