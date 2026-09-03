EXERCISE_OPTIONS = [
    "Squats",
    "Push-ups", 
    "Biceps Curls(dumbbell)",
    "Shoulder Press",
    "Lunges"
    ]
POSE_CONNECTIONS = [
    (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),       # Shoulders & Arms
    (11, 23), (12, 24), (23, 24),                           # Torso / Hips
    (23, 25), (24, 26), (25, 27), (26, 28), (27, 29), (28, 30), (29, 31), (30, 32), (27, 31), (28, 32)  # Legs
]


METRICS_FIELDS = {
    "Squats": {
        "knee_angle": 0,
        "back_angle": 0,
        "depth_status": "N/A",
    },
    "Push-ups": {
        "elbow_angle": 0,
        "body_alignment": "N/A",
        "hip_status": "N/A",
    },
    "Biceps Curls (Dumbbell)": {
        "elbow_angle": 0,
        "shoulder_status": "N/A",
        "swing_status": "N/A",
    },
    "Shoulder Press": {
        "elbow_angle": 0,
        "extension_status": "N/A",
        "back_arch_status": "N/A",
    },
    "Lunges": {
        "front_knee_angle": 0,
        "torso_angle": 0,
        "balance_status": "N/A",
    },
}


PROMPT = (
    "You are Apna AI Coach, a professional AI gym trainer monitoring "
    "a user's workout via live camera.\n\n"

    "Provide ultra-brief, high-energy coaching cues.\n"

    "Maximum ONE sentence and under 12 words.\n"

    "No greetings. No questions. No emojis. No explanations.\n"

    "Speak directly to the user in second person.\n\n"

    "workout_started -> motivational start command.\n"
    "workout_completed -> brief congratulations.\n"
    "set_completed -> praise and tell the user to rest briefly.\n"
    "no_pose_detected -> tell the user to step into the camera frame.\n"
    "ongoing_form_check -> give a direct correction when there is a form issue.\n"
    "ongoing_form_check without issue -> brief motivation.\n\n"

    "Maintain a professional coaching tone and prioritize safety."
)