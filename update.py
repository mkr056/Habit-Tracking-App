from config import update_properties, Habit, URL
import helpers
import json
import requests


def update_title(habit_id=0):
    new_title = helpers.get_title()
    habit_json = json.dumps({'title': new_title})
    response = requests.post(f'{URL}/{habit_id}/update', json=habit_json)
    data = response.json()
    print(data.get('error')) if data.get('error') else print('Habit updated!')


def update_periodicity(habit_id=0):
    new_periodicity = helpers.get_periodicity()
    habit_json = json.dumps({'periodicity': new_periodicity})
    response = requests.post(f'{URL}/{habit_id}/update', json=habit_json)
    data = response.json()
    print(data.get('error')) if data.get('error') else print('Habit updated!')


def update_both(habit_id=0):
    new_title = helpers.get_title()
    new_periodicity = helpers.get_periodicity()
    habit = Habit(new_title, new_periodicity)
    habit_json = json.dumps(habit.__dict__)
    response = requests.post(f'{URL}/{habit_id}/update', json=habit_json)
    data = response.json()
    print(data.get('error')) if data.get('error') else print('Habit updated!')


def get_property_name():
    property_name = input(f"Property name ({'/'.join(update_properties)}): ")
    prepared_property_name = helpers.prepare_string(property_name)
    is_existing_property_name = prepared_property_name in update_properties
    if not is_existing_property_name:
        print("Invalid property name.")
        return get_property_name()
    else:
        return prepared_property_name


properties = {
    'title': update_title,
    'periodicity': update_periodicity,
    'both': update_both
}


def update_habit():
    habit_id = helpers.get_id()
    habits = helpers.get_habits()
    is_existing_id = helpers.check_existing_id(habits, habit_id)
    if is_existing_id:
        property_name = get_property_name()
        property_handler = properties.get(property_name)
        property_handler(habit_id)
    else:
        print("Habit id does not exist.")
