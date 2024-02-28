import json
import requests
import helpers
from config import periodicities, URL


class Habit:
    def __init__(self, title='', periodicity=''):
        self.title = title
        self.periodicity = periodicity


def get_title():
    title = input("Habit title: ")
    stripped_title = title.strip()
    if not stripped_title:
        print("Invalid habit title.")
        return get_title()
    else:
        return stripped_title


def get_periodicity():
    periodicity = input(f"Habit periodicity ({', '.join(periodicities)}): ")
    prepared_periodicity = helpers.prepare_string(periodicity)
    is_existing_periodicity = prepared_periodicity in periodicities
    if not is_existing_periodicity:
        print("Invalid habit periodicity.")
        return get_periodicity()
    else:
        return prepared_periodicity


def create_habit():
    habit_title = get_title()
    habit_periodicity = get_periodicity()
    habit = Habit(habit_title, habit_periodicity)
    habit_json = json.dumps(habit.__dict__)
    response = requests.post(f'{URL}/create', json=habit_json)
    data = response.json()
    print(data.get('error')) if data.get('error') else print('Habit created!')
