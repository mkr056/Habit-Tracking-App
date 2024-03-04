import json
import requests
import helpers
from config import periodicities, URL, Habit


def create_habit():
    habit_title = helpers.get_title()
    habit_periodicity = helpers.get_periodicity()
    habit = Habit(habit_title, habit_periodicity)
    habit_json = json.dumps(habit.__dict__)
    response = requests.post(f'{URL}/create', json=habit_json)
    data = response.json()
    print(data.get('error')) if data.get('error') else print('Habit created!')
