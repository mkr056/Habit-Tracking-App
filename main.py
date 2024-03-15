import db
import common
import random
from datetime import datetime, timedelta
from Habit import Habit
from commands.create import create_habit
from commands.check import check_habit
from commands.update import update_habit
from commands.delete import delete_habit
from commands.info import get_habit_info
from commands.exit import handle_exit


def create_example_data():
    """
    Function to create example data in the database
    """
    # create 5 example habits with random periodicity and random completion_dates
    for i in range(1, 6):
        habit_title = f"test{i}"
        periodicity = random.choice(list(['daily', 'weekly']))  # randomly selected periodicity of the habit
        completion_dates = []
        start_date = datetime.now() - timedelta(weeks=4)  # get timestamp from 4 weeks ago

        # generate timestamps for each day/week over the past 4 weeks with a 70% chance of adding a timestamp.
        # for daily periodicity 28 entries are required and for weekly 4 entries
        for j in range(28 if periodicity == 'daily' else 4):
            if random.random() < 0.7:  # there is a 30 percent chance of skipping habit completion
                completion_dates.append(start_date.strftime(common.DATETIME_FORMAT))
            # skip to the next day or week depending on the periodicity
            start_date += common.time_difference[periodicity]
        # once all the data is formed, create instance and add a new entry to the database
        new_habit = Habit(title=habit_title, periodicity=periodicity, completion_dates=",".join(completion_dates))
        new_habit.create()


def refresh_streaks():
    """
    Function to refresh current and longest streak for all habits in the database
    """
    db_habits = db.get_habits(('all', 'all'))  # get all habits in the database
    # iterate over habits creating corresponding instances based on db data and refreshing streak values for each habit
    for item in db_habits:
        habit_id = item[0]
        periodicity = item[2]
        completion_dates = item[4]
        habit = Habit(periodicity=periodicity, completion_dates=completion_dates)
        habit.refresh_streak(habit_id)


def prompt_user():
    """
    Main function to interact with the user and handle commands
    """
    print("Application has been launched!")
    db.setup_table()  # create table in the database if it does not exist
    db_habits = db.get_habits(('all', 'all'))  # get all habits in the database
    # if there are no habits in the database, then insert example data
    if not db_habits:
        create_example_data()
    # repeat this code until the app is not terminated by the exit command handler
    while True:
        refresh_streaks()  # refresh current and longest streaks for all habit before executing command handlers
        command = input("Enter a command (create/check/update/delete/info/exit): ")  # get command from user
        prepared_command = common.prepare_string(command)  # prepare user command for accessing the handler function
        command_handler = commands.get(prepared_command)  # get handler based on key (command)
        # if handler exists then call it, otherwise print message and start new loop iteration
        if command_handler:
            command_handler()
        else:
            print("Invalid command.")
            continue


# dictionary of all available commands as keys and corresponding handlers as values
commands = {
    'create': create_habit,
    'check': check_habit,
    'update': update_habit,
    'delete': delete_habit,
    'info': get_habit_info,
    'exit': handle_exit
}

if __name__ == '__main__':
    prompt_user()
