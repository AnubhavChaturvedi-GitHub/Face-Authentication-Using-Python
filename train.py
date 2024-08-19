import cv2
import numpy as np
import os

# Load the face recognizer and face detector
recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def get_images_and_labels(data_dir):
    image_paths = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.jpg')]
    faces = []
    labels = []
    label_map = {}
    label_counter = 0

    for image_path in image_paths:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces_detected = face_cascade.detectMultiScale(gray)
        for (x, y, w, h) in faces_detected:
            face = gray[y:y+h, x:x+w]
            
            # Extract label from the filename
            try:
                filename = os.path.basename(image_path)
                label_str = filename.split('.')[1]  # Assuming 'user.<label>.<count>.jpg'
                
                if label_str not in label_map:
                    label_map[label_str] = label_counter
                    label_counter += 1

                label = label_map[label_str]  # Map to numeric ID
                
                faces.append(face)
                labels.append(label)

            except (IndexError, ValueError):
                print(f"Error extracting label from filename: {filename}")
                continue

    return faces, labels

print("Training face recognizer...")
faces, labels = get_images_and_labels('dataset')

if len(faces) == 0 or len(labels) == 0:
    print("No faces found for training. Ensure images are properly labeled and available.")
else:
    recognizer.train(faces, np.array(labels))
    recognizer.save('trainer.yml')
    print("Training complete.")
