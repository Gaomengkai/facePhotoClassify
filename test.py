import numpy as np
import face_recognition as fr

img1 = fr.load_image_file("trump.jpg")
img2 = fr.load_image_file("trump2.jpg")
img3 = fr.load_image_file("obama.jpg")

enc1 = fr.face_encodings(img1)[0]
enc2 = fr.face_encodings(img2)[0]
enc3 = fr.face_encodings(img3)[0]

res = fr.compare_faces([enc1,enc3],enc2)
print(res)
print(type(enc1))
