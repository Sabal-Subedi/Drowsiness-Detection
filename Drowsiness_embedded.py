import socket
import cv2
import mediapipe as mp
import math
import os

def send_ble_alert(command=b"ALERT"):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("localhost", 9999))
        client.sendall(command)
        client.close()
    except Exception as e:
        print(f"Could not send BLE alert: {e}")

def check_for_reset():
    try:
        with open("reset_flag.txt", "r") as f:
            flag = f.read()
        if flag == "1":
            with open("reset_flag.txt", "w") as f:
                f.write("0")
            return True
    except:
        return False
    return False

def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def eye_aspect_ratio(landmarks, eye_indices):
    left = landmarks[eye_indices[0]]
    right = landmarks[eye_indices[3]]
    top = landmarks[eye_indices[1]]
    bottom = landmarks[eye_indices[2]]
    return euclidean(top, bottom) / euclidean(left, right)

def main():
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)

    LEFT_EYE = [33, 159, 145, 133]
    RIGHT_EYE = [362, 386, 374, 263]

    EAR_THRESHOLD = 0.25
    EYE_CLOSED_FRAMES_THRESHOLD = 40
    HEAD_NOD_FRAMES_THRESHOLD = 20
    NOD_THRESHOLD_PIXELS = 30

    eye_closed_frames = 0
    head_nod_frames = 0
    alert_triggered = False
    nod_baseline = None

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if check_for_reset():
            print("Reset signal received from Arduino")
            eye_closed_frames = 0
            head_nod_frames = 0
            alert_triggered = False

        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = [(int(pt.x * w), int(pt.y * h)) for pt in face_landmarks.landmark]

                left_ear = eye_aspect_ratio(landmarks, LEFT_EYE)
                right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE)

                nose_y = landmarks[1][1]
                if nod_baseline is None:
                    nod_baseline = nose_y

                if (nose_y - nod_baseline) > NOD_THRESHOLD_PIXELS:
                    head_nod_frames += 1
                else:
                    head_nod_frames = 0

                if left_ear < EAR_THRESHOLD and right_ear < EAR_THRESHOLD:
                    eye_closed_frames += 1
                else:
                    eye_closed_frames = 0
                    alert_triggered = False

            if eye_closed_frames >= EYE_CLOSED_FRAMES_THRESHOLD:
                if not alert_triggered:
                    print("Drowsiness Detected!")
                    send_ble_alert(b"ALERT")
                    alert_triggered = True

            elif head_nod_frames >= HEAD_NOD_FRAMES_THRESHOLD and eye_closed_frames < EYE_CLOSED_FRAMES_THRESHOLD:
                alert_triggered = False

            cv2.putText(frame, f"Left EAR: {left_ear:.2f}", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, f"Right EAR: {right_ear:.2f}", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, f"Eye Closed Frames: {eye_closed_frames}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, f"Head Nod Frames: {head_nod_frames}", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imshow("Drowsiness Detector", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Create reset flag file if not present
    if not os.path.exists("reset_flag.txt"):
        with open("reset_flag.txt", "w") as f:
            f.write("0")
    main()
# python Drowsiness_embedded.py