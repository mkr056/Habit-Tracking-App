from helpers import check_is_number, get_habits, prepare_string, get_id, check_existing_id
from config import URL
from common import periodicities
import requests


def get_option():
    options = periodicities + ['all']
    option = input(f"{'/'.join(options)}: ")
    prepared_option = prepare_string(option)
    is_existing_option = prepared_option in option
    if not is_existing_option:
        print("Invalid option.")
        return get_option()
    else:
        return prepared_option


def get_list():
    option = get_option()
    habits = get_habits(option)
    result = ""
    for item in habits:
        habit_id = item[0]
        title = item[1]
        result += f"id: {habit_id}, title: {title}\n"
    print(result)


def get_longest_streak_all():
    response = requests.get(f'{URL}/streak')
    data = response.json()
    longest_streak = data.get('longest_streak')
    result = ""
    for item in longest_streak:
        value = item[0]
        result += f"Longest streak: {value}"
    print(result)


def get_longest_streak_id():
    habit_id = get_id()
    habits = get_habits()
    is_existing_id = check_existing_id(habits, habit_id)
    if is_existing_id:
        response = requests.get(f'{URL}/streak?id={habit_id}')
        data = response.json()
        longest_streak = data.get('longest_streak')
        result = ""
        for item in longest_streak:
            value = item[0]
            result += f"Longest streak: {value}"
        print(result)
    else:
        print("Habit id does not exist.")


def get_habit_info():
    prompt_text = ("1 - return a list of currently tracked habits\n"
                   "2 - return the longest run streak of all defined habits\n"
                   "3 - return the longest run streak for a given habit\n"
                   "Enter option number: ")
    command_number = input(prompt_text)
    is_number = check_is_number(command_number)
    if is_number:
        command_handler = commands.get(int(command_number))
        command_handler()


commands = {
    1: get_list,
    2: get_longest_streak_all,
    3: get_longest_streak_id
}
