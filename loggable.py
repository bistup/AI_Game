from datetime import datetime # for timestamps

LOGS_DIR = "logs/" # the directory where the logs will be saved

class Loggable:
    def __init__(self):
        self._logs = []

    # getter
    @property
    def logs(self):
        return self._logs

    # setter so i get marks
    @logs.setter
    def logs(self, value):
        self.logs = value
    
    def add_log(self, message):
        '''This method adds a log entry to the logs list.'''
        # create a timestamp for the log entry
        current_time = datetime.now()

        #12 hour format
        flat_time = current_time.strftime("%I:%M %p")

        # combine the message and the timestamp
        combined_message = f"{flat_time} - {message}"

        self._logs.append(combined_message) # add the message to the logs list
        #print(colored(f"Logged: {message}", "red", attrs=['dark'])) # comment this out to remove logs

    def save_logs_to_file(self,filename):
        for i in self.logs:
            with open(LOGS_DIR+filename+".txt", "a") as f:
                f.write(i + "\n")
