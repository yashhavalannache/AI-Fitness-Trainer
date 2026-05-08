def calculate_calories(weight, height, age, goal):

    # Simple BMR Formula

    bmr = 10 * weight + 6.25 * height - 5 * age + 5

    if goal == "Weight Loss":
        calories = bmr - 300

    elif goal == "Muscle Gain":
        calories = bmr + 300

    else:
        calories = bmr

    return round(calories, 2)