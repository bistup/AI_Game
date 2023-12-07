import json

class Leaderboard:

    def __init__(self):
        with open("Leaderboard.json", "r") as leaderboard: # This opens the json file with 'read' permissions
            self.jsonFile = json.load(leaderboard) # This is the json file that stores the leaderboard

    def checkScore(self, name):
        try:
            print(f"Your score is: {self.jsonFile[name]}")
            return self.jsonFile[name] # This returns the score of the player
        except:
            print("This is your first time playing! Welcome!")
            self.createScore(name) # This creates a new score for the player

    def createScore(self, name):
        self.jsonFile[name] = 0 # This creates a new score for the player with the new name
        self.saveScore() # This saves the score to the json file

    def changeScore(self, name, score):
        self.jsonFile[name] = score
        self.saveScore()

    def saveScore(self):
        with open("leaderboard.json", "w") as leaderboard: # This opens the json file with 'write' permissions
            json.dump(self.jsonFile, leaderboard, indent=2) # This saves the score to the json file


