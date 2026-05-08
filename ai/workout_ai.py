def generate_workout(goal, level):

    workout_plan = {}

    # WEIGHT LOSS

    if goal == "Weight Loss":

        if level == "Beginner":

            workout_plan = {
                "Day 1": "Jump Rope - 15 mins | Squats - 3x12 | Pushups - 3x10",
                "Day 2": "Jogging - 20 mins | Lunges - 3x12 | Plank - 45 sec",
                "Day 3": "Cycling - 20 mins | Burpees - 3x10 | Mountain Climbers"
            }

        elif level == "Intermediate":

            workout_plan = {
                "Day 1": "HIIT - 20 mins | Squats - 4x15 | Pushups - 4x12",
                "Day 2": "Running - 30 mins | Lunges - 4x15 | Plank - 60 sec",
                "Day 3": "Cycling - 30 mins | Burpees - 4x15 | Mountain Climbers"
            }

        else:

            workout_plan = {
                "Day 1": "Advanced HIIT - 30 mins | Weighted Squats",
                "Day 2": "Sprint Intervals | Pushups | Core Circuit",
                "Day 3": "Full Body Conditioning"
            }

    # MUSCLE GAIN

    elif goal == "Muscle Gain":

        if level == "Beginner":

            workout_plan = {
                "Day 1": "Bench Press - 3x10 | Pushups - 3x12",
                "Day 2": "Squats - 3x12 | Lunges - 3x10",
                "Day 3": "Shoulder Press - 3x10 | Plank - 45 sec"
            }

        elif level == "Intermediate":

            workout_plan = {
                "Day 1": "Bench Press - 4x10 | Incline Dumbbell Press",
                "Day 2": "Barbell Squats - 4x12 | Deadlifts",
                "Day 3": "Shoulder Press - 4x10 | Pullups"
            }

        else:

            workout_plan = {
                "Day 1": "Heavy Chest + Triceps",
                "Day 2": "Heavy Legs + Deadlifts",
                "Day 3": "Heavy Back + Biceps"
            }

    # MAINTENANCE

    else:

        workout_plan = {
            "Day 1": "Full Body Workout",
            "Day 2": "Cardio + Core",
            "Day 3": "Strength Training"
        }

    return workout_plan