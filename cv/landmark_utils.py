import mediapipe as mp


def get_landmark_points(landmarks, landmark_names):

    points = []

    for name in landmark_names:

        landmark = getattr(
            mp.solutions.pose.PoseLandmark,
            name
        )

        point = landmarks[landmark.value]

        points.append([point.x, point.y])

    return points