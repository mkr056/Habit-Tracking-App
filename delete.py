import requests
from config import URL
from helpers import get_id, get_habits, check_existing_id


def delete_habit():
    habit_id = get_id()
    habits = get_habits()
    is_existing_id = check_existing_id(habits, habit_id)
    if is_existing_id:
        requests.post(f'{URL}/{habit_id}/delete')
        print('Habit deleted!')
    else:
        print("Habit id does not exist.")