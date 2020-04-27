
import imageFinder
import eval

# get all the images that match for a group with default threshold of 0.5
# for i in range(7):
#     group_id = i+1
#     similar_pics = imageFinder.getImagesForGroup(group_id)
#     eval.avg_precision_recal(similar_pics , group_id)


group_id = 1
similar_pics = imageFinder.getImagesForGroup(group_id)
evaluation = eval.Eval(similar_pics, group_id)
precision = evaluation.precision()
recall = evaluation.recall()

#