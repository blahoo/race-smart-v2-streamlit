import cv2
import PoseModule as pm

# Define ideal angles for body parts
ideal_angles = {
    "right_arm": 60,
    "left_arm": 60,
    "right_leg": 130,
    "left_leg": 130,
    "right_hip": 190,
    "left_hip": 0
}

# Thresholds for angle evaluation
threshold_good = 10  # within 10 degrees
threshold_okay = 20  # within 20 degrees

def evaluate_angle(angle, ideal_angle):
    diff = abs(angle - ideal_angle)
    if diff <= threshold_good:
        return "Good", (0, 255, 0)  # green
    elif diff <= threshold_okay:
        return "Okay", (0, 255, 255)  # yellow
    else:
        return "Bad", (0, 0, 255)  # red

def find_and_adjust_angle(detector, img, p1, p2, p3):
    angle = detector.findAngle(img, p1, p2, p3)
    adjusted_angle = angle if angle <= 180 else 360 - angle
    return adjusted_angle

def func(path):
    img = cv2.imread(path)
    if img is None:
        print("Error: Could not read the image file.")
        return None

    img = cv2.resize(img, (1280, 720))
    detector = pm.poseDetector()
    
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    feedback = []
    if lmList:
        statuses = []
        
        # Right Arm
        angle = detector.findAngle(img, 12, 14, 16)
        status, color = evaluate_angle(angle, ideal_angles["right_arm"])
        statuses.append((f"Right Arm: {status}", color, (50, 50)))
        cv2.circle(img, (lmList[14][1], lmList[14][2]), 10, color, cv2.FILLED)
        cv2.circle(img, (lmList[14][1], lmList[14][2]), 20, color, 2)  # Outline

        # Left Arm
        angle = detector.findAngle(img, 11, 13, 15)
        status, color = evaluate_angle(angle, ideal_angles["left_arm"])
        statuses.append((f"Left Arm: {status}", color, (50, 100)))
        cv2.circle(img, (lmList[13][1], lmList[13][2]), 10, color, cv2.FILLED)
        cv2.circle(img, (lmList[13][1], lmList[13][2]), 20, color, 2)  # Outline

        # Right Leg
        angle = find_and_adjust_angle(detector, img, 24, 26, 28)
        status, color = evaluate_angle(angle, ideal_angles["right_leg"])
        statuses.append((f"Right Leg: {status}", color, (50, 150)))
        cv2.circle(img, (lmList[26][1], lmList[26][2]), 10, color, cv2.FILLED)
        cv2.circle(img, (lmList[26][1], lmList[26][2]), 20, color, 2)  # Outline

        # Left Leg
        angle = find_and_adjust_angle(detector, img, 23, 25, 27)
        status, color = evaluate_angle(angle, ideal_angles["left_leg"])
        statuses.append((f"Left Leg: {status}", color, (50, 200)))
        cv2.circle(img, (lmList[25][1], lmList[25][2]), 10, color, cv2.FILLED)
        cv2.circle(img, (lmList[25][1], lmList[25][2]), 20, color, 2)  # Outline

        # Right Hip
        angle = detector.findAngle(img, 12, 24, 26)
        status, color = evaluate_angle(angle, ideal_angles["right_hip"])
        statuses.append((f"Right Hip: {status}", color, (50, 250)))
        cv2.circle(img, (lmList[24][1], lmList[24][2]), 10, color, cv2.FILLED)
        cv2.circle(img, (lmList[24][1], lmList[24][2]), 20, color, 2)  # Outline
        if angle > 60:
            feedback.append("SHORTEN YOUR STRIDE LENGTH BY %.2f degrees." %(abs(60 - angle)))
        elif angle < 45:
            feedback.append("LENGTHEN YOUR STRIDE BY %.2f degrees to reach optimal stride length." %(45 - angle))

        # Left Hip
        angle = detector.findAngle(img, 11, 23, 25)
        status, color = evaluate_angle(angle, ideal_angles["left_hip"])
        statuses.append((f"Left Hip: {status}", color, (50, 300)))
        cv2.circle(img, (lmList[23][1], lmList[23][2]), 10, color, cv2.FILLED)
        cv2.circle(img, (lmList[23][1], lmList[23][2]), 20, color, 2)  # Outline
        if angle > 120:
            feedback.append("Additionally, you’re heel striking,\nwhich can prevent propulsion and cause injury.\nPoint your foot forward and land in the middle of your foot to correct this.")
        elif angle < 115:
            feedback.append("Additionally, you’re striking,\nwhich is generally used by sprinters and is not effective for healthy distance running.\nConsider flexing your foot to land in the middle.")
    
        # Draw status information
        for text, color, position in statuses:
            x, y = position
            cv2.putText(img, text, (x + 10, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    cv2.imwrite("Posture_Analysis.jpg", img)
    return "\n".join(feedback)

if __name__ == "__main__":
    feedback_text = func("path_to_your_image.jpg")
    if feedback_text:
        print("Feedback:")
        print(feedback_text)