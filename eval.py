# evaluate performance of imageFinder.py
# Precision
# Recall

class Eval:

    def __init__(self):
        self.precision= []
        self.recall = []

    def evaluation(self, similar_pics, group_id):
        print(similar_pics)
        print(group_id)
