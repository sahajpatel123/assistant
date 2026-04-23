import cv2
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
        if filename.endswith(".jpg") or filename.endswith(".png"):
            path = os.path.join(faces_dir, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(os.path.splitext(filename)[0])

    if not known_face_encodings:
        print("No known faces found in 'faces' directory.")
        return False

    video_capture = cv2.VideoCapture(0)
    import time
    time.sleep(1)

    ret, frame = video_capture.read()
    video_capture.release()

    if not ret:
        print("Could not access webcam.")
        return False

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            print(f"User verified: {name}")
            return True

    print("User not recognized. Saving intruder image.")
    cv2.imwrite("intruder.jpg", frame)
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
        subprocess.run(["screencapture", "-x", "-t", "jpg", screen_path], check=True)
        img = Image.open(screen_path)
        
        response = vision_model.generate_content([prompt, img])
        
        # Clean up
        if os.path.exists(screen_path):
            os.remove(screen_path)
            
        return response.text.replace("*", "") # Clean up markdown asterisks for TTS
    except Exception as e:
        print(f"Vision error: {e}")
        return "I encountered an error trying to process the screen feed, Sir."

if __name__ == "__main__":
    if verify_user():
        print("Access Granted")
    else:
        print("Access Denied")
