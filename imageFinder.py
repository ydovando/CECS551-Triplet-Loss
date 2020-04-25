#input: a group id
#intermediate steps: 
        ##1) using the highest p_{c} of the face detection software,
        ##2) store one image for each member in the group. in total, you should have 3 images (1 per group member)

#output: images of group members


# get group id 

from os import walk
import os


from os import walk
import os

from keras_yolo_model import _main_
# from image2vec import calc_embs



photo_dirs = os.getcwd()+"/photos"
weights_path = os.getcwd() +"/yolov3.weights"

def getImagesForGroup(x):
        group_in_query = str(x)
        result = _main_(photo_dirs, weights_path, group_in_query)
        print("BEST PC IMAGES FOR GROUP: " , result)





