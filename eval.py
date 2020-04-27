# evaluate performance of imageFinder.py
# Precision
# Recall
import os

class Eval:

    def __init__(self, similar_pics, group_id):
        self.precision= 0
        self.recall = 0
        self.similar_pics = similar_pics
        self.group_id = group_id
        self.num_correct_imgs= self.correct_images()
        self.recognized_images = len(similar_pics)
        self.act_imgs = self.recall_denom

    def evaluation(self, similar_pics, group_id):
        print(similar_pics)
        print(group_id)

    def correct_images(self):
        photo_dir = os.getcwd()+"/photos"
        correct = 0
        for item in self.similar_pics:
            # first item in tuple (image path, distance)
            image_file_path = item[0]
            # first character in image path
            group_num = image_file_path[0]

            # if the group ids match then it is counted as correct
            if group_num == str(self.group_id):
                correct+=1
        self.num_correct_imgs = correct
    

    def recall_denom(self):

        photo_dir = os.getcwd()+"/photos"
        act_imgs = 0
        for dir in os.listdir(photo_dir):
            img_dirs = photo_dir+"/"+dir

            for img in os.listdir(img_dirs):
                if dir[0] == str(self.group_id):
                    act_imgs +=1
        self.act_imgs = act_imgs


    # number of correctly recognized images /  number of recognized images
    def precision(self):
        self.precision =self.num_correct_imgs * 100 / self.recognized_images
        return self.precision
    
    # number of correctly recognized images /  number of actual images in the group
    def recall(self):
        self.recall =self.num_correct_imgs * 100 / self.act_imgs
        return self.recall



        

                