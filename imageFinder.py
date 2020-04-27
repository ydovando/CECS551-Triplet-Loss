#input: a group id
#intermediate steps: 
        ##1) using the highest p_{c} of the face detection software,
        ##2) store one image for each member in the group. in total, you should have 3 images (1 per group member)

#output: images of group members


# get group id 
from os import walk
import os
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from imageio import imread
from skimage.transform import resize
from scipy.spatial import distance
from keras.models import load_model
import numpy as np

import keras_yolo_model 
import image2vec 


import pandas as pd


photo_dirs = os.getcwd()+"/photos"
weights_path = os.getcwd() +"/yolov3.weights"


class ImageFinder:
        def __init__(self):
                self.result=[]
        def getImagesForGroup(self, x , dist_thresh=0.5):

                path_to_embeds = os.getcwd()+"/embed-vecs.csv"

                if os.path.exists(path_to_embeds) == False:
                        # ------------------------------- [ FIND TOP PC PICTURES OF GROUP MEMBERS ] ------------------------------
                        group_in_query = str(x)
                        self.result = keras_yolo_model._main_(photo_dirs, weights_path, group_in_query)
                        f = open("vectors.txt", "w")



                        # ---------------------------------- [GETTING ALL THE EMBEDDED VECTORS] ---------------------------
                        all_embedded_vectors_dict = {}
                        file_names = []
                        count = 0

                        for dir in os.listdir(photo_dirs):

                                data = {}

                                image_dirpath = photo_dirs+"/"+dir
                                image_filepaths = [os.path.join(image_dirpath, f)
                                                for f in os.listdir(image_dirpath)]
                                embs = image2vec.calc_embs(image_filepaths)
                                for i in range(len(image_filepaths)):
                                        data['{}{}'.format(dir, i)] = {'image_filepath': image_filepaths[i],
                                                                        'emb': embs[i]}
                                        file_names.append(image_filepaths[i])

                                X = []
                                for v in data.values():
                                        X.append(v['emb'])
                                pca = PCA(n_components=3).fit(X)

                                X_Me = []
                                print("xme: ", dir)
                                for k, v in data.items():
                                        print("k: ", k)
                                        if dir in k:
                                                X_Me.append(v['emb'])

                                Xd_Me = pca.transform(X_Me)

                                img_count = 0
                                for i in Xd_Me:
                                        print(str(file_names[count]), " ", img_count, " ",
                                                Xd_Me[img_count, :]/Xd_Me[img_count, :].sum(axis=0, keepdims=1))
                                        all_embedded_vectors_dict.update(
                                                {str(file_names[count]): Xd_Me[img_count, :]/Xd_Me[img_count, :].sum(axis=0, keepdims=1)})
                                        f.write(str(file_names[count]))
                                        f.write(" ")
                                        f.write(str(Xd_Me[img_count, :] /
                                                        Xd_Me[img_count, :].sum(axis=0, keepdims=1)))
                                        f.write("\n")
                                        img_count += 1
                                        count += 1

                        f.close()
                # ---------------------------- [GETTING ALL PICS SIMILAR TO THE GROUP MEMBERS] ---------------------------------------
        

                similar_pics =[]

                if os.path.exists(path_to_embeds) == False:
                        df = pd.DataFrame.from_dict(all_embedded_vectors_dict , orient= 'index' , columns = ['x','y','z'])
                        for item in result:
                                # get the image path 
                                top_pc_image_path = item[1]
                                print(top_pc_image_path)
                                #get the embedded vector associated with that image
                                vec_top_pc = np.array(df.loc[top_pc_image_path][-3:])
                                print("Top pc array: " , vec_top_pc)

                                counter = 0
                                for dir in os.listdir(photo_dirs):
                                        image_dirpath = photo_dirs+"/"+dir
                                        for img in os.listdir(image_dirpath):
                                                image_filepath = os.path.join(image_dirpath, img)

                                                if top_pc_image_path != image_filepath:
                                                        vec_compare= np.array(df.loc[image_filepath][-3:])
                                                        distance = image2vec.calc_dist_using_vecs(vec_top_pc, vec_compare)
                                                        if distance < dist_thresh:
                                                                similar_pics.append((image_filepath, distance))  
                        df.to_csv(os.getcwd()+"/embed-vecs.csv")
                        return similar_pics

                else:
                        print("EMBEDDING VECTORS CSV FILE EXISTS")
                        group_in_query = str(x)
                        self.result = keras_yolo_model._main_(photo_dirs, weights_path, group_in_query)

                        data = pd.read_csv(os.getcwd()+"/embed-vecs.csv", index_col=0)
                        similar_pics = []
                        for top in self.result:
                                image_path_interest = top[1]
                                vec_top_pc = np.array(data.loc[image_path_interest][-3:])

                                for dir in os.listdir(photo_dirs):
                                        image_dirpath = photo_dirs+"/"+dir
                                        for img in os.listdir(image_dirpath):
                                                image_filepath = os.path.join(image_dirpath, img)
                                                if image_path_interest != image_filepath:
                                                        vec_compare= np.array(data.loc[image_filepath][-3:])
                                                        distance = image2vec.calc_dist_using_vecs(vec_top_pc, vec_compare)
                                                        if distance < dist_thresh:
                                                                similar_pics.append((image_filepath, distance))      
                        return similar_pics




                

