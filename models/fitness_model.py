from models import db

class FitnessProgress(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, nullable=False)

    workouts_completed = db.Column(db.Integer, default=0)

    streak_days = db.Column(db.Integer, default=0)

    fitness_score = db.Column(db.Integer, default=50)

    calories_burned = db.Column(db.Integer, default=0)

    water_intake = db.Column(db.Float, default=0)

    sleep_hours = db.Column(db.Float, default=0)