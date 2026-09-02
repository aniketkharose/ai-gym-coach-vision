from core.base_exercise import BaseExercise


class SquatDetector(BaseExercise):

    DOWN_THRESHOLD = 100
    UP_THRESHOLD = 160
    MIN_VISIBILITY = 0.7

    # MediaPipe Pose landmark IDs
    LEFT_HIP = 23
    LEFT_KNEE = 25
    LEFT_ANKLE = 27

    RIGHT_HIP = 24
    RIGHT_KNEE = 26
    RIGHT_ANKLE = 28

    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12

    def __init__(self):
        super().__init__()

    def reset(self):
        self.reps = 0
        self.stage = None

    def process(self, landmarks):

        # --------------------------------------------------
        # 1. Calculate left knee angle
        # --------------------------------------------------
        left_knee_angle = self.calculate_angle(
            self.get_point(landmarks, self.LEFT_HIP),
            self.get_point(landmarks, self.LEFT_KNEE),
            self.get_point(landmarks, self.LEFT_ANKLE)
        )

        # --------------------------------------------------
        # 2. Calculate right knee angle
        # --------------------------------------------------
        right_knee_angle = self.calculate_angle(
            self.get_point(landmarks, self.RIGHT_HIP),
            self.get_point(landmarks, self.RIGHT_KNEE),
            self.get_point(landmarks, self.RIGHT_ANKLE)
        )

        # --------------------------------------------------
        # 3. Check visibility of both knees
        # --------------------------------------------------
        left_vis = landmarks[self.LEFT_KNEE].visibility
        right_vis = landmarks[self.RIGHT_KNEE].visibility

        # --------------------------------------------------
        # 4. Select the more visible side
        # --------------------------------------------------
        if left_vis >= right_vis:
            knee_angle = left_knee_angle

            hip_idx = self.LEFT_HIP
            knee_idx = self.LEFT_KNEE
            ankle_idx = self.LEFT_ANKLE
            shoulder_idx = self.LEFT_SHOULDER

        else:
            knee_angle = right_knee_angle

            hip_idx = self.RIGHT_HIP
            knee_idx = self.RIGHT_KNEE
            ankle_idx = self.RIGHT_ANKLE
            shoulder_idx = self.RIGHT_SHOULDER

        # --------------------------------------------------
        # 5. Calculate back / torso angle
        # --------------------------------------------------
        back_angle = self.calculate_angle(
            self.get_point(landmarks, shoulder_idx),
            self.get_point(landmarks, hip_idx),
            self.get_point(landmarks, knee_idx)
        )

        # --------------------------------------------------
        # 6. Check important landmarks visibility
        # --------------------------------------------------
        key_landmark_visible = (
            landmarks[hip_idx].visibility >= self.MIN_VISIBILITY
            and landmarks[knee_idx].visibility >= self.MIN_VISIBILITY
            and landmarks[ankle_idx].visibility >= self.MIN_VISIBILITY
        )

        # --------------------------------------------------
        # 7. Detect DOWN → UP movement
        # --------------------------------------------------
        if key_landmark_visible:

            # User went down
            if knee_angle < self.DOWN_THRESHOLD:
                self.stage = "down"

            # User came back up
            if (
                knee_angle >= self.UP_THRESHOLD
                and self.stage == "down"
            ):
                self.stage = "up"
                self.reps += 1

        # --------------------------------------------------
        # 8. Determine squat depth status
        # --------------------------------------------------
        if self.stage == "down":

            if knee_angle <= self.DOWN_THRESHOLD:
                depth_status = "GOOD DEPTH"
            else:
                depth_status = "TOO HIGH"

        elif self.stage == "up":
            depth_status = "STANDING"

        else:
            depth_status = "N/A"

        # --------------------------------------------------
        # 9. Return metrics
        # --------------------------------------------------
        return {
            "reps": self.reps,
            "knee_angle": int(knee_angle),
            "back_angle": int(back_angle),
            "depth_status": depth_status
        }