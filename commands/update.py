import json
import requests
from config import URL
from common import Habit
import helpers


def update_title(habit_id=0):
    """
    Updates the title of the habit based on user input
    :param habit_id: id of the habit to update
    :return: message to the user
    """
    new_title = helpers.get_title()  # get new habit title from the user
    habit_json = json.dumps({'title': new_title})  # create JSON based on new title
    response = requests.post(f'{URL}/{habit_id}/update', json=habit_json)  # send request with JSON as body of the request
    data = response.json()  # get JSON data from response
    # if there has been a json schema error then print it, otherwise print success message
    print(data.get('error')) if data.get('error') else print('Habit updated!')


def update_periodicity(habit_id=0):
    """
    Updates the periodicity of the habit based on user input
    :param habit_id: id of the habit to update
    :return: message to the user
    """
    new_periodicity = helpers.get_periodicity()  # get new habit periodicity from the user
    habit_json = json.dumps({'periodicity': new_periodicity})  # create JSON based on new periodicity
    response = requests.post(f'{URL}/{habit_id}/update', json=habit_json)  # send request with JSON as body of the request
    data = response.json()  # get JSON data from response
    # if there has been a json schema error then print it, otherwise print success message
    print(data.get('error')) if data.get('error') else print('Habit updated!')


def update_both(habit_id=0):
    """
    Updates the title and periodicity of the habit based on user input
    :param habit_id: id of the habit to update
    :return: message to the user
    """
    new_title = helpers.get_title()  # get new habit title from the user
    new_periodicity = helpers.get_periodicity()  # get new habit periodicity from the user
    habit = Habit(new_title, new_periodicity)  # create a new Habit instance
    habit_json = json.dumps(habit.__dict__)  # convert instance to JSON
    response = requests.post(f'{URL}/{habit_id}/update', json=habit_json)  # send request with JSON as body of the request
    data = response.json()  # get JSON data from response
    # if there has been a json schema error then print it, otherwise print success message
    print(data.get('error')) if data.get('error') else print('Habit updated!')


def get_property_name():
    """
    Gets option (property) regarding habit update from the user
    :return: option (property) entered by the user
    """
    update_properties = properties.keys()  # list of all possible options (properties)
    property_name = input(f"Property name ({'/'.join(update_properties)}): ")  # get property name from the user
    prepared_property_name = helpers.prepare_string(property_name)  # prepare property for check
    is_existing_property_name = prepared_property_name in update_properties  # check if entered property is valid
    # if entered property is not of the allowed options then repeat the process, otherwise return prepared property
    if not is_existing_property_name:
        print("Invalid property name.")
        return get_property_name()
    else:
        return prepared_property_name


def update_habit():
    """
    Updates habit properties in the database (triggered when update command is received)
    :return: message to the user
    """
    habit_id = helpers.get_id()  # get habit id from the user
    habits = helpers.get_habits()  # get all habits in the database
    is_existing_id = helpers.check_existing_id(habits, habit_id)  # check if received id exists in the database
    # if id exists then prompt user for property name and call corresponding handler, otherwise print error message
    if is_existing_id:
        property_name = get_property_name()
        property_handler = properties.get(property_name)
        property_handler(habit_id)
    else:
        print("Habit id does not exist.")


# a dictionary of all available options for updating a habit as keys and corresponding handlers as values
properties = {
    'title': update_title,
    'periodicity': update_periodicity,
    'both': update_both
}
