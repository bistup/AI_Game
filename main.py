from game import Game

if __name__ == "__main__":
    game = Game()
    game.run()

    print("Game Logs:\n ")
    for log in (game.loggable.logs):
        print(log)

    print("\n")

    print("Error Logs:\n ")
    for eLog in (game.eLogs):
        print(eLog)