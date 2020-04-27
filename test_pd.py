import pandas as pd
import os
import numpy as np
import image2vec
data = pd.read_csv(os.getcwd()+"/embed-vecs.csv", index_col=0)


photo_dirs = os.getcwd() + "/photos"

similar_pics = []
image_path_interest = photo_dirs + "/4-Yashua-Ovando/yash-1.jpg"
vec_top_pc = np.array(data.loc[image_path_interest][-3:])
print(vec_top_pc)

for dir in os.listdir(photo_dirs):

    image_dirpath = photo_dirs+"/"+dir
    for img in os.listdir(image_dirpath):
        image_filepath = os.path.join(image_dirpath, img)
        if image_path_interest != image_filepath:
            vec_compare= np.array(data.loc[image_filepath][-3:])
            distance = image2vec.calc_dist_using_vecs(vec_top_pc, vec_compare)
            if distance < 0.4:
                print(distance)

                similar_pics.append((image_filepath, distance))

print(similar_pics)
