import json
import requests
import helpers
from config import URL
from common import Habit


def create_habit():
    """
    Creates new habit in the database (triggered when create command is received)
    :return: message to the user
    """
    habit_title = helpers.get_title()  # get habit title from the user
    habit_periodicity = helpers.get_periodicity()  # get habit periodicity from the user
    habit = Habit(habit_title, habit_periodicity)  # create a new Habit instance
    habit_json = json.dumps(habit.__dict__)  # convert instance to JSON
    response = requests.post(f'{URL}/create', json=habit_json)  # send request with JSON as body of the request
    data = response.json()  # get JSON data from response
    # if there has been a json schema error then print it, otherwise print success message
    print(data.get('error')) if data.get('error') else print('Habit created!')
