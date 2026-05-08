import cv2
import mediapipe as mp
import numpy as np

from pose_detector import PoseDetector

detector = PoseDetector()

cap = cv2.VideoCapture(0)

count = 0
position = None
feedback = "Start Squat"

def calculate_angle(a, b, c):

    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
              np.arctan2(a[1]-b[1], a[0]-b[0])

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


while True:

    success, frame = cap.read()

    if not success:
        break

    frame, results = detector.find_pose(frame)

    try:

        landmarks = results.pose_landmarks.landmark

        hip = [
            landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x,
            landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y
        ]

        knee = [
            landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].x,
            landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].y
        ]

        ankle = [
            landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].x,
            landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].y
        ]

        angle = calculate_angle(hip, knee, ankle)

        # Squat Logic

        if angle > 160:

            position = "UP"
            feedback = "Go Lower ⬇️"

        if angle < 90 and position == "UP":

            position = "DOWN"
            count += 1
            feedback = "Perfect Squat 🔥"

        if 90 <= angle <= 160:

            feedback = "Keep Going 👍"

        # Display Angle

        cv2.putText(
            frame,
            f'Angle: {int(angle)}',
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

        # Rep Counter

        cv2.putText(
            frame,
            f'Squats: {count}',
            (50,100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,0,0),
            2
        )

        # Feedback

        cv2.putText(
            frame,
            feedback,
            (50,150),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,255),
            2
        )

    except:
        pass

    cv2.imshow("AI Squat Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()