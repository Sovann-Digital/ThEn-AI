import cv2 
import face_recognition
import numpy as np
import json
import os

# Function to load user data from JSON file
def load_user_data(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

# Function to encode faces from images in the database
def encode_faces(database_path):
    encodings = []
    names = []
    print("Encoding (～￣▽￣)～...!")
    for image_file in os.listdir(database_path):
        name = os.path.splitext(image_file)[0]
        image_path = os.path.join(database_path, image_file)
        image = cv2.imread(image_path)
        if image is not None:
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_image)
            if face_locations:
                face_encoding = face_recognition.face_encodings(rgb_image, [face_locations[0]])[0]
                encodings.append(face_encoding)
                names.append(name)
                print(f"Encoded {name}")
            else:
                print(f"No face found in {name}")
        else:
            print(f"Unable to read {image_file}")
    return encodings, names

# Function to capture video and recognize faces
def capture_and_recognize(encodings, names, user_data):
    cap = cv2.VideoCapture(0)
    print("Starting Face Recognition...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        if face_locations:
            face_encodings = face_recognition.face_encodings(rgb_small_frame, [face_locations[0]])[0]
            face_distances = face_recognition.face_distance(encodings, face_encodings)
            closest_match_index = np.argmin(face_distances)
            closest_match_distance = face_distances[closest_match_index]
            matched_name = names[closest_match_index] if face_distances[closest_match_index] < 0.6 else "Unknown"
            if matched_name in user_data["User"]:
                name_label = user_data["User"][matched_name]["name"]
            else:
                name_label = matched_name
            cv2.putText(frame, f'{name_label} {round(closest_match_distance, 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.rectangle(frame, (face_locations[0][3]*4, face_locations[0][0]*4), (face_locations[0][1]*4, face_locations[0][2]*4), (255, 0, 255), 2)
            cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    print("Program Starting...\n")
    database_path = 'Resources/database'
    user_data_path = 'Resources/data/data.json'
    user_data = load_user_data(user_data_path)
    encodings, names = encode_faces(database_path)
    capture_and_recognize(encodings, names, user_data)
