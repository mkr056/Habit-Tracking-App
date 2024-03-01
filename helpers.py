import requests
from config import URL


def prepare_string(string):
    return string.strip().lower()


def check_is_number(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def check_existing_id(ids, habit_id):
    return any(habit_id in row for row in ids)


def get_id():
    habit_id = input("Habit id: ")
    is_number = check_is_number(habit_id)
    if not is_number:
        print("Invalid habit id.")
        return get_id()
    else:
        return int(habit_id)


def get_ids():
    response = requests.get(f'{URL}/ids')
    data = response.json()
    return data.get('ids')