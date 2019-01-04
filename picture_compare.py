import face_recognition
import os



known_image_path = os.path.join('snapShots','SnapShot9.jpg' )
unknown_image_path = os.path.join('images', 'known_faces', 'Kwasi.jpg')


known_image = face_recognition.load_image_file(known_image_path)
unknown_image = face_recognition.load_image_file(unknown_image_path)

known_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([known_encoding], unknown_encoding)

print(results)

