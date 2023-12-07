
class CrimeScene:
    def __init__(self, location):
        self.location = location
        self.__clues = [] # private
        self.__investigated = False # private

    # getter
    @property
    def investigated(self):
        return self.__investigated

    # setter
    @investigated.setter
    def investigated(self, value):
        if isinstance(value, bool):
            self.__investigated = value
        else:
            print("investigated is expected to be a boolean.")

    def add_clue(self, clue):
        """This method adds clues to the crime scene investigation."""
        self.__clues.append(clue)

    def review_clues(self):
        """At the moment there are no checks on who can see the clues. We
        might need some further protection here."""
        return self.__clues
    