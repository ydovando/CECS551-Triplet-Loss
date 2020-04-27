
import imageFinder
import eval


meanAP =0


# query 1  threshold = 0.5 for all groups
print( "QUERY 1: -----------------------------------------------------------")
print("Threshold 0.5")
print()
precision_sum = 0
for i in range(7):
    group_id = i+1 
    similar_pics = imageFinder.getImagesForGroup(group_id)
    evaluation = eval.Eval(similar_pics, group_id)
    precision = evaluation.precision()
    print("Precision for query 1 and group id ", group_id, " ", precision)
    precision_sum += precision
    recall = evaluation.recall()
    print("Recall for query 1 and group id ", groupid , " " , recall)
meanAP += (precision_sum / 7)

print( "--------------------------------------------------------------")


#query 2 threshold = 0.4 for all groups
print( "QUERY 2: -----------------------------------------------------------")
print("Threshold 0.4")
print()
precision_sum = 0

for i in range(7):
    group_id = i+1 
    similar_pics = imageFinder.getImagesForGroup(group_id , 0.4)
    evaluation = eval.Eval(similar_pics, group_id)
    precision = evaluation.precision()
    print("Precision for query 2 and group id ", group_id, " ", precision)
    precision_sum += precision
    recall = evaluation.recall()
    print("Recall for query 2 and group id ", groupid , " " , recall)
meanAP += (precision_sum / 7)
print( "--------------------------------------------------------------")



# query 3 threshold = 0.3 for all group 
print( "QUERY 3: -----------------------------------------------------------")
print("Threshold 0.3")
Print()

precision_sum = 0
for i in range(7):
    group_id = i+1 
    similar_pics = imageFinder.getImagesForGroup(group_id , 0.3)
    evaluation = eval.Eval(similar_pics, group_id)

    precision = evaluation.precision()
    print("Precision for query 3 and group id ", group_id, " ", precision)
    precision_sum += precision

    recall = evaluation.recall()
    print("Recall for query 3 and group id ", groupid , " " , recall)
meanAP += (precision_sum / 7)

print( "--------------------------------------------------------------")
print()
print()
meanAP = meanAP / 3
print("Mean Average Precision: " , meanAP)

