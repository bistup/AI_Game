import random

class Minigame:
    def key_guessing_game(self):
        # Generates random number for key between 1 and 3
        key = random.randint(1, 3) 
        
        while True:
            # prompts user to guess the key
            guess = int(input("Guess which number reveals the clue(1/2/3): "))
            
            # check if guess is correct
            if guess == key:
                print("Congratulations! You guessed the correct number! The clue has been revealed, press e.")
                return True # returns true if the guess is correct
            else:
                print("Wrong number! Try again.")
            

