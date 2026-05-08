import cv2
import mediapipe as mp
import time

from cv.exercise_config import EXERCISES
from cv.pose_utils import calculate_angle
from cv.landmark_utils import get_landmark_points
from cv.feedback_engine import get_feedback

# MediaPipe Setup

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

mp_draw = mp.solutions.drawing_utils

# Exercise State

exercise_count = 0
exercise_position = None

# Plank Timer

plank_start_time = None


def process_exercise(frame, exercise_name):

    global exercise_count
    global exercise_position
    global plank_start_time

    # ====================================
    # UNSUPPORTED EXERCISE
    # ====================================

    if exercise_name not in EXERCISES:

        plank_start_time = None

        cv2.putText(
            frame,
            "Exercise Not Supported",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        return frame

    # Exercise Config

    config = EXERCISES[exercise_name]

    # Reset plank timer for rep exercises

    if config["type"] != "static":

        plank_start_time = None

    # Convert to RGB

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Pose Detection

    results = pose.process(rgb)

    if results.pose_landmarks:

        # Draw Skeleton

        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        try:

            landmarks = results.pose_landmarks.landmark

            # Get Required Points

            points = get_landmark_points(
                landmarks,
                config["landmarks"]
            )

            # Angle Calculation

            angle = calculate_angle(
                points[0],
                points[1],
                points[2]
            )

            # ====================================
            # REP EXERCISES
            # ====================================

            if config["type"] == "rep":

                if angle > config["up_angle"]:

                    exercise_position = "UP"

                if (
                    angle < config["down_angle"]
                    and exercise_position == "UP"
                ):

                    exercise_position = "DOWN"

                    exercise_count += 1

            # ====================================
            # FEEDBACK
            # ====================================

            feedback = get_feedback(
                angle,
                config,
                exercise_position
            )

            # ====================================
            # EXERCISE NAME
            # ====================================

            cv2.putText(
                frame,
                f'Exercise: {exercise_name}',
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            # ====================================
            # REP EXERCISES DISPLAY
            # ====================================

            if config["type"] == "rep":

                cv2.putText(
                    frame,
                    f'Count: {exercise_count}',
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    2
                )

            # ====================================
            # STATIC EXERCISES DISPLAY
            # ====================================

            elif config["type"] == "static":

                # Start Timer

                if plank_start_time is None:

                    plank_start_time = time.time()

                elapsed_time = int(
                    time.time() - plank_start_time
                )

                cv2.putText(
                    frame,
                    f'Time: {elapsed_time} sec',
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    2
                )

            # ====================================
            # ANGLE DISPLAY
            # ====================================

            cv2.putText(
                frame,
                f'Angle: {int(angle)}',
                (50, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            # ====================================
            # FEEDBACK DISPLAY
            # ====================================

            cv2.putText(
                frame,
                feedback,
                (50, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

        except:
            pass

    return frame