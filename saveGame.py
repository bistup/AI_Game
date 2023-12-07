import pickle
SAVE_DIR = "saves/"

class SaveGame:
    def save_game(self, saveName, saveData):
        """This method saves the game state to a file."""
        f = open(SAVE_DIR+saveName, "wb") # wb = write binary
        pickle.dump(saveData.__dict__, f, 2) # 2 = binary format, dumps the game state to the file
        f.close() # close the file

    
    def load_game(self, saveName):
        """This method loads the game state from a file."""
        f = open(SAVE_DIR+saveName, "rb") # rb = read binary
        saveData = pickle.load(f) # loads the game state from the file
        f.close() # close the file
        return saveData # return the game state