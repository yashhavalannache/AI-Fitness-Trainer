from flask import Blueprint, render_template
from ai.workout_data import WORKOUT_DETAILS

workout = Blueprint("workout", __name__)

# =========================
# SHOW ALL WORKOUT DAYS
# =========================
@workout.route("/workout")
def workout_page():

    return render_template(
        "workout.html",
        workout_plan=WORKOUT_DETAILS,
        active_page="workout"
    )


# =========================
# SHOW SINGLE DAY DETAILS
# =========================
@workout.route("/workout/<day>")
def workout_details(day):

    details = WORKOUT_DETAILS.get(day)

    if not details:
        return "Workout not found", 404

    return render_template(
        "workout_details.html",
        day=day,
        details=details,
        active_page="workout"
    )