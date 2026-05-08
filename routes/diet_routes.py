from flask import Blueprint, render_template
from ai.diet_ai import generate_diet
from datetime import datetime

diet = Blueprint('diet', __name__)

@diet.route('/diet')
def diet_page():

    diet_plan = generate_diet("Muscle Gain")

    day = datetime.today().strftime("%A")

    today_diet = diet_plan.get(day, {})

    return render_template(
        'diet.html',
        diet_plan=diet_plan,
        today_diet=today_diet,
        day=day,
        active_page="diet"
    )