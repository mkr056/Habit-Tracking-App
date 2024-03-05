import requests
from config import URL
from common import periodicities


def prepare_string(string):
    return string.strip().lower()


def check_is_number(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def check_existing_id(habits, habit_id):
    return any(sublist[0] == habit_id for sublist in habits)


def get_title():
    new_title = input("Enter title: ")
    stripped_title = new_title.strip()
    if not stripped_title:
        print("Invalid habit title.")
        return get_title()
    else:
        return stripped_title


def get_periodicity():
    periodicity = input(f"Habit periodicity ({'/'.join(periodicities)}): ")
    prepared_periodicity = prepare_string(periodicity)
    is_existing_periodicity = prepared_periodicity in periodicities
    if not is_existing_periodicity:
        print("Invalid habit periodicity.")
        return get_periodicity()
    else:
        return prepared_periodicity


def get_id():
    habit_id = input("Habit id: ")
    is_number = check_is_number(habit_id)
    if not is_number:
        print("Invalid habit id.")
        return get_id()
    else:
        return int(habit_id)


def get_habits(periodicity='all'):
    response = requests.get(f'{URL}/habits?periodicity={periodicity}')
    data = response.json()
    return data.get('habits')