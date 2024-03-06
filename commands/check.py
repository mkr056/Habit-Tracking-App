import requests
from config import URL
from helpers import get_id, get_habits, check_existing_id


def check_habit():
    """
    Checks habit as completed in the database (triggered when check command is received )
    :return: message to the user
    """
    habit_id = get_id()  # get habit id from the user
    habits = get_habits()  # get all habits in the database
    is_existing_id = check_existing_id(habits, habit_id)  # check if received id exists in the database
    # if id exists then send request and print success message, otherwise print error message
    if is_existing_id:
        requests.post(f'{URL}/{habit_id}/check')  # sends request to the server to check/complete a habit with given id
        print('Habit checked!')
    else:
        print("Habit id does not exist.")