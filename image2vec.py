# input: an image (x) which includes a human face
# intermediate step: Find bounding box of the face in the input
# output: embedding  vector (f(X) in R ^{d}) in d-dimensional Euclidean space of the bounding box.
# the embedding vector should be normalized ||f(x)||_{2} = sum( f_{i}(x)^2) =1 from i to d

import sys
import numpy as np
import os
import matplotlib.pyplot as plt
import cv2
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from imageio import imread
from skimage.transform import resize
from scipy.spatial import distance
from keras.models import load_model
import csv



def prewhiten(x):
    if x.ndim == 4:
        axis = (1, 2, 3)
        size = x[0].size
    elif x.ndim == 3:
        axis = (0, 1, 2)
        size = x.size
    else:
        raise ValueError('Dimension should be 3 or 4')

    mean = np.mean(x, axis=axis, keepdims=True)
    std = np.std(x, axis=axis, keepdims=True)
    std_adj = np.maximum(std, 1.0/np.sqrt(size))
    y = (x - mean) / std_adj
    return y

def l2_normalize(x, axis=-1, epsilon=1e-10):
    output = x / np.sqrt(np.maximum(np.sum(np.square(x), axis=axis, keepdims=True), epsilon))
    return output

def load_and_align_images(filepaths, margin):
    cascade_path = './model/cv2/haarcascade_frontalface_alt2.xml'
    cascade = cv2.CascadeClassifier(cascade_path)
    
    aligned_images = []
    for filepath in filepaths:

        print(filepath)
        img = imread(filepath)

        faces = cascade.detectMultiScale(img,
                                         scaleFactor=1.1,
                                         minNeighbors=1)
        (x, y, w, h) = faces[0]
        cropped = img[y-margin//2:y+h+margin//2,
                      x-margin//2:x+w+margin//2, :]
        aligned = resize(cropped, (160, 160), mode='reflect')
        aligned_images.append(aligned)
            
    return np.array(aligned_images)

def calc_embs(filepaths, margin=10, batch_size=1):
    model_path = './model/keras/model/facenet_keras.h5'
    model = load_model(model_path)
    aligned_images = prewhiten(load_and_align_images(filepaths, margin))
    pd = []
    for start in range(0, len(aligned_images), batch_size):
        pd.append(model.predict_on_batch(aligned_images[start:start+batch_size]))
    embs = l2_normalize(np.concatenate(pd))
    return embs

def calc_dist(img_name0, img_name1):
    return distance.euclidean(data[img_name0]['emb'], data[img_name1]['emb'])

def calc_dist_using_vecs(vec_top_pc, vec_compare):
    return distance.euclidean(vec_top_pc, vec_compare)

def calc_dist_plot(img_name0, img_name1):
    print(calc_dist_using(img_name0, img_name1))
    plt.subplot(1, 2, 1)
    plt.imshow(imread(data[img_name0]['image_filepath']))
    plt.subplot(1, 2, 2)
    plt.imshow(imread(data[img_name1]['image_filepath']))

def export_embedded_vector():

    f = open("vectors.txt", "w")
    all_embedded_vectors_dict = {}
    file_names = []
    count = 0
    print("export start")
    image = os.getcwd() + image_dir_basepath
    for x in os.listdir(image):
        export_data = {}
        export_names = [x]
        print(export_names)
        for name in export_names:
            print(name)
            # image_dirpath = os.path.join(image_dir_basepath, x)
            image_dirpath = image_dir_basepath + x
            image_filepaths = [os.path.join(image_dirpath, f) for f in os.listdir(image_dirpath)]
            embs = calc_embs(image_filepaths)
            for i in range(len(image_filepaths)):
                # print(image_filepaths[i])
                export_data['{}{}'.format(name, i)] = {'image_filepath' : image_filepaths[i],
                                                'emb' : embs[i]}
                file_names.append(image_filepaths[i])
        X = []
        for v in export_data.values():
            X.append(v['emb'])
        pca = PCA(n_components=3).fit(X)

        X_Me = []
        print("xme:" + x)
        # print (export_data.items())
        for k, v in export_data.items():
            print("k: " + k)
            if x in k:
                X_Me.append(v['emb'])
        
        Xd_Me = pca.transform(X_Me)
        img_count = 0
        for i in Xd_Me:
            print(str(file_names[count]), " ", img_count, " ", Xd_Me[img_count,:]/Xd_Me[img_count,:].sum(axis=0,keepdims=1))
            all_embedded_vectors_dict.update({str(file_names[count]): Xd_Me[img_count,:]/Xd_Me[img_count,:].sum(axis=0,keepdims=1)})
            f.write(str(file_names[count]))
            f.write(" ")
            f.write(str(Xd_Me[img_count,:]/Xd_Me[img_count,:].sum(axis=0,keepdims=1)))
            f.write("\n")
            img_count += 1
            count += 1
    f.close()

# photo = str(sys.argv[1])
# head_tail = os.path.split(photo)
# cascade_path = './model/cv2/haarcascade_frontalface_alt2.xml'

# image_dir_basepath = './photos/'
# names = [head_tail[0]]
# image_size = 160

# i = 0
# image_index = 0
# for x in os.listdir(os.path.join(image_dir_basepath, names[0])):
#     if x == head_tail[1]:
#         image_index = i
#         break
#     i += 1



# data = {}
# print(names)
# for name in names:
#     print(name)
#     image_dirpath = image_dir_basepath + name
#     image_filepaths = [os.path.join(image_dirpath, f) for f in os.listdir(image_dirpath)]
#     embs = calc_embs(image_filepaths)
#     for i in range(len(image_filepaths)):
#         data['{}{}'.format(name, i)] = {'image_filepath' : image_filepaths[i],
#                                         'emb' : embs[i]}

# # calc_dist_plot('4-Matthew-Nguyen0', '4-Matthew-Nguyen1')

# X = []
# for v in data.values():
#     X.append(v['emb'])
# pca = PCA(n_components=3).fit(X)

# X_Me = []
# for k, v in data.items():
#     print("k: " + k)
#     if head_tail[0] in k:
#         print("got here 1")
#         X_Me.append(v['emb'])
        
# Xd_Me = pca.transform(X_Me)

# fig = plt.figure(figsize=(8,8))
# ax = fig.add_subplot(111, projection='3d')
# plt.rcParams['legend.fontsize'] = 10   
# # ax.plot(Xd_Me[0, 0], Xd_Me[0, 1], Xd_Me[0, 2],
# #         'o', markersize=8, color='purple', alpha=0.5, label='Me')
# print()
# nev = Xd_Me[image_index,:]/Xd_Me[image_index,:].sum(axis=0,keepdims=1)
# print(nev)
# print(nev.sum())
# plt.title('Embedding Vector')
# ax.legend(loc='upper right')

# # export_embedded_vector()
# # plt.show()