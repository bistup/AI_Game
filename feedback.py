# Caitriona McCann
# 01/12/2023

class Feedback:
    def __init__(self):
        self.feedback = []

    def get_feedback(self, feedback):
        self.feedback.append(feedback)

    def print_feedback(self):
        #if there is nothing in feedback print out msg
        if len(self.feedback) == 0:
            print("You haven't entered any feedback yet")
        #To print the feedback weve collected
        else:
            print("!!!!! Feedback !!!!!")
            for i in range(len(self.feedback)):
                print(f"{i + 1}. {self.feedback[i]}")
            print("!!!!!!!!!!!!!!!!!!!!")

