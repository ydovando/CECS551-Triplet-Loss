
import imageFinder
import eval
#initialize evaluation 
evaluation = eval.Eval()

# get all the images that match for a group with default threshold of 0.5
# for i in range(7):
#     group_id = i+1
#     similar_pics = imageFinder.getImagesForGroup(group_id)
#     eval.avg_precision_recal(similar_pics , group_id)

group_id = 5
similar_pics = imageFinder.getImagesForGroup(group_id)
print(similar_pics)