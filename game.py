################################################################################
# CMPU 2023 OOP – TU 857 - Semester 1 Assignment.
# Group: OOPs I did it again

# Members:
# 1. Keith Salhani (student ID: C22322811).
# 2. Limani (student ID: C22334951).
# 3. Ben Mc Carron (student ID: C22394893).
# 4. Jennifer Bishop (student ID: C22363246).
# 5. Caitriona McCann (student ID: C22408674).
# Date: October 20, 2023.
# Game Expansion Explanation:
#
# In this expansion of our mystery game, "<Insert Story>," All stories are
# Fully generated by AI using the OpenAI API GPT3.5 Turbo.
# We also addeed an option to save, and load your game.
# We added a leaderboard to keep track of your score.
# We added a feedback system to get feedback from the player.
# We added a minigame to the game.
# We added a log system to log the players interactions.
# We added a clue system to the game.
# File Structure:
# - main.py: The script that starts them all
# - game.py: Module containing the Game class.
# - crimeScene.py: Module containing the CrimeScene class.
# - loggable.py: Module containing the Loggable class.
# - saveGame.py: Module containing the SaveGame class.
# - story.py: Module containing the Story class.
# - feedback.py: Module containing the Feedback class.
# - Leaderboard.py: Module containing the Leaderboard class.
# - minigame.py: Module containing the Minigame class.
# - requirements.txt: File containing the required packages.
# - config.json: Configuration file for the game.
# - stories: Folder containing the stories.
# - saves: Folder containing the save files.
#
# Running the Game:
# - To play "<Insert Story>" with our exciting expansions, 
# run pip install -r requirements.txt,
# - run the main.py script.
# ensure that game.py, crimeScene.py, loggable.py, saveGame.py, story.py,
# feedback.py, Leaderboard.py, minigame.py, stories, and 
# saves are in the same directory.
#
# Enjoy the game and have fun becoming the ultimate detective!
#
# Important Note:
# Please keep this header unaltered in all submitted files.
################################################################################

from termcolor import colored # for colored text
from art import tprint # for the title
from abc import ABC, abstractmethod # for abstract classes
import os # for the file system
import json # for the json files
import climage # for the image

from loggable import Loggable # for logging player interactions
from crimeScene import CrimeScene # for the crime scene
from saveGame import SaveGame # for saving the game
from story import Story # for the story generation
from Leaderboard import Leaderboard # for the leaderboard
from minigame import Minigame # for the minigame
from feedback import Feedback # for the feedback system

with open("config.json", "r") as f:
    config = json.load(f)
    AI_GENERATED = config["AI_Generated"]

# The Exception characters
class Character(ABC):
    """ The Character class serves as the base class, providing common
    attributes and methods for characters. The Suspect and Witness classes
    are subclasses that inherit from Character and introduce their unique
    attributes and methods. """

    def __init__(self, name, dialogue, mood):
        self._name = name # Protected attribute
        self._dialogue = dialogue # Protected attribute
        self._interacted = False # Protected attribute
        self._mood = mood # Protected attribute

    # if it is not of benefit for the design of the system
    # you do not need to explicitely provide getter and setter
    # methods. Instead, the behavior methods might be sufficient,
    # as I have chosen in this case.
    
    def interact(self):
        pass
    
    @abstractmethod
    def perform_action(self):
        pass

class Suspect(Character):
    """This is a special type of character. This is the suspect in our crime
    investigation."""

    def __init__(self, name, dialogue, confirmedBy, mood):
        super().__init__(name, dialogue, mood=mood)  # Call the constructor of the base class
        self._confirmedBy = confirmedBy  # Add the unique attribute for Suspect

    @property
    def susDesc(self):
        return self._confirmedBy
    
    def interact(self):
        if not self._interacted:
            interaction = f"{self._name}: {self._dialogue}\n - {self._confirmedBy}"
            self._interacted = True
        else:
            interaction = f"{self._name} is no longer interested in talking."

        return interaction
    
    def perform_action(self):
        # this piece of code is a monstrocity. Do not read it.
        # There is an fstring within an fstring
        # I didnt even know that was possible
        print(f"\n {colored(f'Suspect {self._name}', 'red')} :",
               colored(f"{self._dialogue}\n - {self._confirmedBy}\n", "green", attrs=['bold']), colored("-"+self._mood, "red"))
        return(f"Suspect {self._name}: {self._dialogue} - {self._confirmedBy}")

class Witness(Character):
    """This class is the witness. This person has either seen or heard
    something to do with the crime."""
    def __init__(self, name, dialogue, description, mood):
        super().__init__(name, dialogue, mood=mood)  # Call the constructor of the base class
        self._description = description  # Add the unique attribute for Suspect

    @property
    def whoConfirmed(self):
        return self._description
    
    def interact(self):
        if not self._interacted:
            interaction = f"{self._name}: {self._dialogue}\n - {self._confirmedBy}"
            self._interacted = True
        else:
            interaction = f"{self._name} is no longer interested in talking."

        return interaction
    
    def perform_action(self):
        print(colored(f"Witness {self._name}","blue"), ":",
               colored(f"{self._dialogue}\n - Description: {self._description}\n", "green", attrs=['bold']), colored("-"+self._mood, "red"))

        return(f"Witness {self._name}: {self._dialogue} - Description: {self._description}")

class NPC(Character):
    def __init__(self, name, dialogue, mood):
        super().__init__(name, dialogue, mood=mood)  # Call the constructor of the base class

    def perform_action(self):
        print(colored(f"NPC {self._name}", "cyan"), colored(f": {self._dialogue}", "green" , attrs=['bold']) , colored("-"+self._mood, "red"), "\n")
        return(f"NPC {self._name}: {self._dialogue}")

crime_scene = CrimeScene("")

class Game:
    """The Game class interacts with the other objects to facilitate game
    play."""

    def __init__(self):
        self.running = True
        self.game_started = False
        self.characters_interacted = False
        self.crime_scene = crime_scene
        self.lbObject = Leaderboard()
        self.feedback = Feedback()
        self.minigame = Minigame()

        #its 3AM again

        self.clueSelected = 0 # door selection input
        self.currentScene = 'Lobby' # tracks current scene
        self.peopleSpokenTo = False
        self.NPCsSpokenTo = False
        self.clues_investigated = {} # dictionary to keep track of investigated rooms
        self.clues = [] # state the scene names that exist


        self.loggable = Loggable() # For logging player interactions
        self.__eloggable = Loggable() # For logging errors
        self.loggable.add_log("Game started")

        story_files = []
        i=1
        for files in os.listdir("stories"):
            if(files.endswith('.json')):
                print(f"{i}. {files}")
                story_files.append(f"stories/{files}")
                i+=1
        
        print(f"{i}. Generate New Story")

        try:
            load_story_input = int(input(colored("Which story would you like to play? ", "white")))
        except:
            self.__eloggable.add_log("Error: Invalid input")
            load_story_input = 1


        if(load_story_input == i): # If the user wants to generate a new story (always the last option)
            story = Story()
            print("Generating story...")
            story_title = story.make_story()
            if(story_title == 0): # If the story generation failed
                story_title = story_files[load_story_input-2] # Load the default story
                self.__eloggable.add_log("Error: AI Generated story failed, loading default story") # Log the error
        else:
            story_title = story_files[load_story_input-1] # Load the story the user selected

        with open(story_title, "r") as f:
            self.story = json.load(f) # load the AI generated JSON

            self.suspect = Suspect(self.story["characters"]["suspect"]["name"], # Get the name
                                   self.story["characters"]["suspect"]["alibi"], # Get the alibi
                                   self.story["characters"]["suspect"]["confirmation"],
                                   self.story["characters"]["suspect"]["mood"]) # Get the confirmation
            
            self.witness = Witness(self.story["characters"]["witness"]["name"], 
                                   self.story["characters"]["witness"]["observation"], 
                                   self.story["characters"]["witness"]["description"],
                                   self.story["characters"]["witness"]["mood"])
            
            self.NPC_one = NPC(self.story["characters"]["npcs"][0]["name"], # Get the name
                               self.story["characters"]["npcs"][0]["dialogue"], # Get the dialogue
                               self.story["characters"]["npcs"][0]["mood"]) # Get the mood
            self.NPC_two = NPC(self.story["characters"]["npcs"][1]["name"], 
                               self.story["characters"]["npcs"][1]["dialogue"], 
                               self.story["characters"]["npcs"][1]["mood"])
            
            for i in self.story["clues"]: # Get the clues
                self.clues_investigated[i] = False
                self.clues.append(i)


        self.save_files = {} # Dictionary to look at all the save files

        load_save_input = input(colored("Would you like to load a save file (y/n)? ", "white"))
        if(load_save_input.lower() == "y"):
            for i, files in enumerate(os.listdir("saves"),1):
                print(f"{i}. {files}")
                self.save_files[i] = files
            
            try:
                self.save_input = int(input("Enter the number of the save file you would like to load: "))
                save_dict = SaveGame.load_game(self, self.save_files[self.save_input]) # Get the save file
                self.__dict__.update(save_dict) # Update the Game classes variables with save vars
            except:
                self.__eloggable.add_log("Error: Invalid input")
                print("Loading default save")

    @property
    def eLogs(self):
        return self.__eloggable.logs
    
    def run(self):
        tprint(self.story["title"]) # Print the title in ascii
        for i in self.story["story"]: # Print the story
            print(i)

        img = climage.convert('stories/'+self.story["title"]+".png") # Convert the story image to ascii i think
        print(img) # Print the image


        while self.running:
            self.update()

    def update(self):
        if not self.game_started:
            # Python wont throw an error if we enter a number
            # Because its taking the input as a string
            # so we dont have to worry about the program crashing
            try:
                player_input = input(colored("Press 'q' to quit or 's' to start:\n ","white"))
                if player_input.lower() == "q": 
                    self.running = False
                elif player_input.lower() == "s":
                    self.game_started = True
                    self.start_game()
            except KeyboardInterrupt as ke: # check if user pressed ctrl C
                self.__eloggable.add_log("Error: User interrupted program (CTRL+C).")
            except Exception as e: # catch all other errors
                self.__eloggable.add_log(f"Error: {e}")

        else:
            player_input = input(colored("Press 'q' to quit, 'c' to continue, "
                                 "'i' to interact, 'e' to examine clues, "
                                 "'r' to review your clues, "
                                 "'L' to look at the logs, "
                                 "'f' to finish your investigation, "
                                 "or 'clues' to look at clues: ", "white"))
            if player_input.lower() == "q":
                save_input = input("Would you like to save the game (y/n)?")
                if(save_input.lower() == "y"):
                    save_name = str(input(f"Enter the save name \n(enter {self.save_files[self.save_input]} to overwrite current save): "))
                    SaveGame.save_game(self, save_name, self) # Save the game

                print("Would you like to save the logs (y/n)?")
                save_logs = str(input())
                if save_logs.lower() == "y":
                    filename = str(input("Enter the filename: "))
                    self.loggable.save_logs_to_file(filename) # Save the interaction logs
                    self.__eloggable.save_logs_to_file(str("Error_")+filename) # Save the error logs
                    
                self.running = False # End the game
            elif player_input.lower() == "c":
                self.continue_game()
            elif player_input.lower() == "i":
                self.interact_with_characters()
            elif player_input.lower() == "e":
                self.examine_clues()
            elif player_input.lower() == "r":
                clues = self.crime_scene.review_clues()
                if clues:
                    print(colored(clues,"light_yellow"))
                else:
                    print(colored("You have not found any clues yet."),"red")
            elif player_input.lower() == "l":
                print(self.loggable.logs)
            elif player_input.lower() == "clues":
                self.choose_door()
            elif player_input.lower() == "f":
                self.finish_game()
            
            self.loggable.add_log(f"Input: {player_input}")

    def start_game(self):
        self.player_name = input(colored("Enter your detective's name: ", "white")) # Get the players name
        self.lbObject.checkScore(self.player_name) # Check the leaderboard for the players score
        colored_player_name = colored(str(self.player_name), "white") # Color the players name
        print(f"Welcome, Detective {colored_player_name}!") # Welcome the player
        #print("You find yourself in the opulent drawing room of a grand "
        #      "mansion.")
        #print("As the famous detective, you're here to solve the mysterious "
        #      "case of...")
        #print("'The Missing Diamond Necklace'.")
        #print("Put your detective skills to the test and unveil the truth!")
        

    def finish_game(self):
        user_decisions = {}
        ending_message = []
        for i in self.story["characters"]:
            if i == "npcs":
                for npc in self.story["characters"]["npcs"]:
                    user_input = input(f"Is {npc['name']} innocent? (y/n): ")
                    if(user_input.lower() == "y"): user_input = True
                    elif(user_input.lower() == "n"): user_input = False

                    if user_input and npc['innocent']: # True True
                        user_decisions[npc['name']] = True
                        ending_message.append(colored(f"{npc['name']} is innocent", "green"))
                    elif user_input and not npc['innocent']: # True False
                        user_decisions[npc['name']] = False
                        ending_message.append(colored(f"{npc['name']} is Guilty", "red"))
                    elif not user_input and npc['innocent']: # False True
                        user_decisions[npc['name']] = False
                        ending_message.append(colored(f"{npc['name']} is Innocent", "red"))
                    elif not user_input and not npc['innocent']: # False False
                        user_decisions[npc['name']] = True
                        ending_message.append(colored(f"{npc['name']} is Guilty", "green"))
            else:
                user_input = input(f"Is {self.story['characters'][i]['name']} innocent? (y/n): ")
                if(user_input.lower() == "y"): user_input = True
                elif(user_input.lower() == "n"): user_input = False

                if user_input and self.story['characters'][i]['innocent']: # True True
                    user_decisions[self.story['characters'][i]['name']] = True
                    ending_message.append(colored(f"{self.story['characters'][i]['name']} is innocent", "green"))
                elif user_input and not self.story['characters'][i]['innocent']: # True False
                    user_decisions[self.story['characters'][i]['name']] = False
                    ending_message.append(colored(f"{self.story['characters'][i]['name']} is Guilty", "red"))
                elif not user_input and self.story['characters'][i]['innocent']: # False True
                    user_decisions[self.story['characters'][i]['name']] = False
                    ending_message.append(colored(f"{self.story['characters'][i]['name']} is Innocent", "red"))
                elif not user_input and not self.story['characters'][i]['innocent']: # False False
                    user_decisions[self.story['characters'][i]['name']] = True
                    ending_message.append(colored(f"{self.story['characters'][i]['name']} is Guilty", "green"))

        if all(user_decisions.values()):
            print(colored("You have solved the mystery! You have arrested all the correct suspects!", "green"))
            currentScore = self.lbObject.checkScore(self.player_name) # Check the leaderboard for the players score
            self.lbObject.changeScore(self.player_name, currentScore+100) # Change the players score
        else:
            for i in ending_message:
                print(i)

        #Feedback code from feedback.py
        print("!!!!! Feedback !!!!!")
        
        user_feedback = input("Enter in feedback (or press enter to skip):")
        if user_feedback:
            self.feedback.get_feedback(user_feedback)
            print("Thank you for your input on the game!")

        self.feedback.print_feedback()

        save_input = input("Would you like to save the game (y/n)?")
        if(save_input.lower() == "y"):
            save_name = str(input(f"Enter the save name \n(enter {self.save_files[self.save_input]} to overwrite current save): "))
            SaveGame.save_game(self, save_name, self) # Save the game

        print("Would you like to save the logs (y/n)?")
        save_logs = str(input())
        if save_logs.lower() == "y":
            filename = str(input("Enter the filename: "))
            self.loggable.save_logs_to_file(filename) # Save the interaction logs
            self.__eloggable.save_logs_to_file(str("Error_")+filename) # Save the error logs
        self.running = False

        

           
    def interact_with_characters(self):
        """The interact_with_characters method within the Game class
        demonstrates the interaction with characters, where each
        character's dialogue and unique actions (e.g., providing an alibi,
        sharing an observation) are
        displayed. """

        try:
            userInput = int(input(colored("Press 1 to interact with the witness and suspect.\nPress 2 to interact with the NPCs: ", "white")))
            #userMessage = str(input(colored(f"What would you like to say? \n {self.player_name}: ", 'white')))
            #sentiment = sentiment_pipeline(userMessage)
            #sentiment = sentiment[0].get('label')
            #if(sentiment == 'NEGATIVE'): 
            #    print(colored("They witnesses and suspects refuse to speak to you because you are rude!", 'red')) 
            #    return
            
            if(userInput == 1):
                if(self.peopleSpokenTo): 
                    print("You have spoken to the people already - they no longer wish to speak to you")
                    return

                characters = [self.suspect, self.witness]
                for character in characters:
                    self.loggable.add_log(character.perform_action())
                self.peopleSpokenTo = True
            elif(userInput == 2):
                if(self.NPCsSpokenTo): 
                    print("You have spoken to the NPCs already - they no longer wish to speak to you")
                    return
                characters = [self.NPC_one, self.NPC_two]
                for character in characters:
                    self.loggable.add_log(character.perform_action())
                self.NPCsSpokenTo = True
        except ValueError as ve:
            self.__eloggable.add_log(f"Error: {ve}")
        


    def examine_clues(self):
        if not self.crime_scene.investigated:
            for key, value in self.story["clues"].items(): # For every clue in the story
                if(self.currentScene == key and not self.clues_investigated[self.currentScene]): # If the current scene is the same as the key and the door has not been investigated
                    self.loggable.add_log(f"You investigate {key} and find {value}") # Log the investigation
                    print(colored(f"You investigate {key} - You find {value}","light_yellow")) # Print the investigation
                    self.crime_scene.add_clue(value) # Add the clue to the crime scene
                    self.clues_investigated[self.currentScene] = True # Set the door to investigated
                    return # Exit the function
                
            print(f"Already investigated {self.currentScene}") 
            self.clues_investigated[self.currentScene] = True

            if(not any(self.clues_investigated) == True):
                self.crime_scene.investigated = True
            else:
                print("You've already examined the crime scene clues.")


    def enter_room(self):
        for i, value in enumerate(self.clues, 1): # For every door in the room
            if(self.clueSelected == i): 
                self.loggable.add_log(f">> {value}")
                print(f">> {value}")

    def choose_door(self):
        """This method handles the door examination option. User input is
        being handled. Wrong user input is being handled via print outs for error
        handling."""

        for i, value in enumerate(self.clues, 1):
            print(colored(f"{i}. {value} "))

        try:
            self.clueSelected = int(input()) # Get the door the user wants to enter as an INT
            self.currentScene = self.clues[self.clueSelected-1] # Set the current scene to the door the user selected
            if(self.minigame.key_guessing_game()): # If the user wins the minigame
                self.enter_room() # Enter the room
        except IndexError as ie:
            self.__eloggable.add_log(f"Error: door {self.clueSelected} - {ie}") # Log the error
        except ValueError as ve:
            self.__eloggable.add_log(f"Error: {ve}") # Log the error

        

    def continue_game(self):
        self.loggable.add_log("You continue your investigation, determined to solve the mystery...")
        print("You continue your investigation, determined to solve the mystery...")