import cv2
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import face_recognition
import os
import subprocess
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    vision_model = genai.GenerativeModel('gemini-1.5-flash')
else:
    vision_model = None


def verify_user():
    """
    Captures a frame from the webcam and checks if it matches any known face in the 'faces' directory.
    Returns True if a match is found, False otherwise. If False, saves an intruder image.
    """
    known_face_encodings = []
    known_face_names = []

    faces_dir = "faces"
    if not os.path.exists(faces_dir):
        return False

    for filename in os.listdir(faces_dir):
        if filename.endswith((".jpg", ".png")):
            path = os.path.join(faces_dir, filename)
            image = face_recognition.load_image_file(path)
            # Use multiple jitters/upsamples for a better encoding template
            encodings = face_recognition.face_encodings(
                image, num_jitters=10, model="large")
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(os.path.splitext(filename)[0])

    if not known_face_encodings:
        print("No known faces found in 'faces' directory.")
        return False

    video_capture = cv2.VideoCapture(0)
    import time
    time.sleep(1)

    # Capture 5 frames and use the best one or average
    frames = []
    for _ in range(5):
        ret, f = video_capture.read()
        if ret:
            frames.append(f)
        time.sleep(0.1)

    video_capture.release()

    if not frames:
        print("Could not access webcam.")
        return False

    # Process frames with higher upsampling for accuracy
    for frame in frames:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(
            rgb_frame, number_of_times_to_upsample=2, model="cnn")
        face_encodings = face_recognition.face_encodings(
            rgb_frame, face_locations, model="large")

        for face_encoding in face_encodings:
            # lower tolerance = stricter matching
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding, tolerance=0.45)
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                print(f"User verified with high accuracy: {name}")
                return True

    print("User not recognized. Saving intruder image.")
    cv2.imwrite("intruder.jpg", frames[-1])
    return False


def capture_and_analyze_screen(prompt="What do you see on my screen?"):
    """
    Captures the screen and uses Gemini Vision to answer a prompt about it.
    """
    if not vision_model:
        return "I am sorry Sir, but my visual processing unit is offline. Please configure my API key."

    screen_path = "screen_capture.jpg"
    try:
        # Capture screen on MacOS silently
        subprocess.run(["screencapture", "-x", "-t",
                       "jpg", screen_path], check=True)
        img = Image.open(screen_path)

        response = vision_model.generate_content([prompt, img])

        # Clean up
        if os.path.exists(screen_path):
            os.remove(screen_path)

        # Clean up markdown asterisks for TTS
        return response.text.replace("*", "")
    except Exception as e:
        print(f"Vision error: {e}")
        return "I encountered an error trying to process the screen feed, Sir."


if __name__ == "__main__":
    if verify_user():
        print("Access Granted")
    else:
        print("Access Denied")
