
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
precision = evaluation.precision
recall = evaluation.recall

print(precision)
print(recall)



no_queries = 3
meanAP =0



# # query 1  threshould = 0.5 for all groups
# precision_sum = 0
# for i in range(7):
#     group_id = i+1 
#     similar_pics = imageFinder.getImagesForGroup(group_id)
#     evaluation = eval.Eval(similar_pics, group_id)
#     precision_sum += evaluation.precision()
#     recall = evaluation.recall()
#     print("Recall for query 1 and group id ", groupid , " " , recall)
    
# evalutaiton_1 = eva.Eval(simila)




#query 2 threshold = 04 for all groups




# query 3 threshold = 0.3 for all group 



