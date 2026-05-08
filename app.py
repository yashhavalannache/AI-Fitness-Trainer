from flask import Flask, render_template, session, redirect, url_for, request, flash
from datetime import datetime
import cv2
import os

from models import db
from models.user_model import User
from models.fitness_model import FitnessProgress

from ai.workout_ai import generate_workout
from ai.diet_ai import generate_diet

from utils.bmi import calculate_bmi
from utils.calorie import calculate_calories

from routes.auth_routes import auth
from routes.workout_routes import workout
from routes.diet_routes import diet
from routes.posture_routes import posture

from werkzeug.utils import secure_filename

# =========================
# FLASK APP
# =========================
app = Flask(__name__)

# =========================
# SECRET KEY
# =========================
app.secret_key = "fitness_secret_key"

# =========================
# BASE DIRECTORY
# =========================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# =========================
# DATABASE CONFIG
# =========================
db_path = os.path.join(BASE_DIR, "database.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# =========================
# UPLOAD FOLDER
# =========================
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/uploads")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# INIT DATABASE
# =========================
db.init_app(app)

# =========================
# BLUEPRINTS
# =========================
app.register_blueprint(auth)
app.register_blueprint(workout)
app.register_blueprint(diet)
app.register_blueprint(posture)

# =========================
# GLOBAL CAMERA
# =========================
camera = None

# =========================
# HOME
# =========================
@app.route('/')
def home():
    return render_template('index.html')

# =========================
# DASHBOARD
# =========================
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if not user:
        session.clear()
        return redirect(url_for('login'))

    progress = FitnessProgress.query.filter_by(user_id=user.id).first()

    if not progress:

        progress = FitnessProgress(
            user_id=user.id,
            workouts_completed=0,
            streak_days=0,
            calories_burned=0,
            fitness_score=0
        )

        db.session.add(progress)
        db.session.commit()

    bmi = calculate_bmi(user.weight, user.height)

    calories = calculate_calories(
        user.weight,
        user.height,
        user.age,
        user.goal
    )

    workout_plan = generate_workout(user.goal, user.level)

    diet_plan = generate_diet(user.goal)

    day = datetime.today().strftime("%A")

    today_diet = diet_plan.get(day)

    return render_template(
    'dashboard.html',
    user=user,
    bmi=bmi,
    calories=calories,
    workout_plan=workout_plan,
    diet_plan=diet_plan,
    today_diet=today_diet,
    day=day,
    progress=progress,
    active_page="dashboard"
)

# =========================
# COMPLETE WORKOUT
# =========================
@app.route('/complete_workout', methods=['POST'])
def complete_workout():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    progress = FitnessProgress.query.filter_by(user_id=user.id).first()

    progress.workouts_completed += 1
    progress.streak_days += 1
    progress.calories_burned += 150
    progress.fitness_score = min(progress.fitness_score + 5, 100)

    db.session.commit()

    return redirect(url_for('dashboard'))

# =========================
# STOP CAMERA
# =========================
@app.route("/stop_camera")
def stop_camera():

    global camera

    if camera is not None:
        camera.release()
        camera = None

    return "Camera stopped"

# =========================
# ACCOUNT PAGE
# =========================
@app.route('/account')
def account():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    return render_template('account.html', user=user)

# =========================
# UPDATE ACCOUNT
# =========================
@app.route('/update_account', methods=['POST'])
def update_account():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    user.name = request.form['name']
    user.age = request.form['age']
    user.weight = request.form['weight']
    user.height = request.form['height']
    user.goal = request.form['goal']

    db.session.commit()

    flash("Profile updated successfully ✨", "success")
    flash("Profile picture uploaded successfully 📸", "success")
    flash("Invalid credentials", "error")
    flash("Email not registered", "error")

    return redirect(url_for('account'))

# =========================
# DELETE ACCOUNT
# =========================
@app.route('/delete_account', methods=['POST'])
def delete_account():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if user:

        # =========================
        # DELETE PROFILE IMAGE FILE
        # =========================
        if user.profile_pic:

            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                user.profile_pic
            )

            if os.path.exists(file_path):
                os.remove(file_path)

        # =========================
        # DELETE FITNESS DATA
        # =========================
        FitnessProgress.query.filter_by(user_id=user.id).delete()

        # =========================
        # DELETE USER
        # =========================
        db.session.delete(user)
        db.session.commit()

    # IMPORTANT: flash BEFORE clearing session
    flash("Account deleted successfully 🗑️", "success")

    # clear session AFTER flash is stored
    session.clear()

    return redirect(url_for('home'))


# =========================
# PROFILE IMAGE UPLOAD
# =========================
@app.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    file = request.files.get('profile_pic')

    if not file:
        flash("No file selected")
        return redirect(url_for('account'))

    if file.filename == '':
        flash("Empty filename")
        return redirect(url_for('account'))

    filename = secure_filename(file.filename)

    # UNIQUE IMAGE NAME
    filename = f"user_{user.id}_{filename}"

    save_path = os.path.join(
        app.config['UPLOAD_FOLDER'],
        filename
    )

    file.save(save_path)

    # SAVE IN DATABASE
    user.profile_pic = filename

    db.session.commit()

    flash("Profile picture uploaded successfully 📸")

    return redirect(url_for('account'))


#=================LOGIN========================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        # =========================
        # CHECK EMAIL FIRST
        # =========================
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not registered ❌")
            return redirect(url_for('login'))

        # =========================
        # CHECK PASSWORD
        # =========================
        if user.password != password:
            flash("Invalid password ⚠️")
            return redirect(url_for('login'))

        # =========================
        # SUCCESS LOGIN
        # =========================
        session['user_id'] = user.id
        session['username'] = user.name

        return redirect(url_for('dashboard'))

    return render_template('login.html')

# =========================
# LOGOUT
# =========================
@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('home'))

# =========================
# RUN APP
# =========================
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)