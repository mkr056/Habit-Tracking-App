import requests
from config import URL
from helpers import get_id, get_ids, check_existing_id


def delete_habit():
    habit_id = get_id()
    ids = get_ids()
    is_existing_id = check_existing_id(ids, habit_id)
    if is_existing_id:
        requests.post(f'{URL}/{habit_id}/delete')
        print('Habit deleted!')
    else:
        print("Habit id does not exist.")