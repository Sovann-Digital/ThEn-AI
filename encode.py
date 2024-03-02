import cv2
import face_recognition
import json
import os

def encode_faces(database_path):
    encodings = {}
    print("Encoding Faces...")
    for image_file in os.listdir(database_path):
        name = os.path.splitext(image_file)[0]
        image_path = os.path.join(database_path, image_file)
        image = cv2.imread(image_path)
        if image is not None:
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_image)
            if face_locations:
                face_encoding = face_recognition.face_encodings(rgb_image, [face_locations[0]])[0]
                encodings[name] = face_encoding.tolist()
                print(f"Encoded {name}")
            else:
                print(f"No face found in {name}")
        else:
            print(f"Unable to read {image_file}")
    with open('data/Resources/data/encodings.json', 'w') as file:
        json.dump(encodings, file)
    print("Encodings saved to 'encodings.json'.")

if __name__ == '__main__':
    database_path = 'data/Resources/database'
    encode_faces(database_path)
