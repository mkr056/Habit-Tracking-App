import common
from Habit import Habit


def create_habit():
    """
    Function to create new habit in the database (triggered when create command is received)
    :return: message to the user
    """
    habit_title = common.get_title()  # get habit title from the user
    habit_periodicity = common.get_periodicity()  # get habit periodicity from the user
    habit = Habit(habit_title, habit_periodicity)  # create a new Habit instance
    habit.create()
    print('Habit created!')
