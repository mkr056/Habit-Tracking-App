import db
from Habit import Habit
from common import get_id


def check_habit():
    """
    Function to check habit as completed in the database (triggered when check command is received )
    :return: message to the user
    """
    habit_id = get_id()  # get habit id from the user
    db_habit = db.get_habit((habit_id,))
    # if id exists then send request and print success message, otherwise print error message
    if db_habit:
        habit = Habit(periodicity=db_habit[2], completion_dates=db_habit[4])
        habit.check(habit_id)
        print('Habit checked!')
    else:
        print("Habit id does not exist.")
        check_habit()
