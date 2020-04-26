
from keras_facenet import FaceNet
import os
embedder = FaceNet()
photo_dirs = os.getcwd()+"/photos"

for dir in os.listdir(photo_dirs):
        person_dir = photo_dirs+"/"+dir
        for photo in os.listdir(person_dir):   
            image_path = person_dir+"/"+photo
            print(image_path)
        # embeddings = embedder.embeddings(image)