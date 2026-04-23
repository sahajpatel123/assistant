import cv2
import face_recognition
import os

def verify_user():
    """
    Captures a frame from the webcam and checks if it matches any known face in the 'faces' directory.
    Returns True if a match is found, False otherwise.
    """
    known_face_encodings = []
    known_face_names = []

    # Load known faces
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

    # Initialize webcam
    video_capture = cv2.VideoCapture(0)
    
    # Give the camera some time to warm up
    import time
    time.sleep(1)

    ret, frame = video_capture.read()
    video_capture.release()

    if not ret:
        print("Could not access webcam.")
        return False

    # Find faces in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            print(f"User verified: {name}")
            return True

    print("User not recognized.")
    return False

if __name__ == "__main__":
    # Test
    if verify_user():
        print("Access Granted")
    else:
        print("Access Denied")
