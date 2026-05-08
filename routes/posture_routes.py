from flask import Blueprint, render_template, Response, request
import cv2

from cv.engine import process_exercise

posture = Blueprint('posture', __name__)

cap = cv2.VideoCapture(0)


def generate_frames(exercise):

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame = process_exercise(
            frame,
            exercise
        )

        ret, buffer = cv2.imencode('.jpg', frame)

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )


@posture.route('/posture')
def posture_page():

    exercise = request.args.get(
        'exercise',
        'squat'
    )

    return render_template(
        'posture.html',
        exercise=exercise,
        active_page="posture"
    )


@posture.route('/video_feed/<exercise>')
def video_feed(exercise):

    return Response(
        generate_frames(exercise),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )