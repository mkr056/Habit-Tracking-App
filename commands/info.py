import requests
from helpers import check_is_number, get_habits, prepare_string, get_id, check_existing_id
from config import URL
from common import periodicities


def get_option():
    """
    Gets periodicity option (for optional filtering) from the user and checks if it is one of the possible values
    :return: prepared periodicity option
    """
    options = periodicities + ['all']  # add 'all' option to the list of possible periodicities
    option = input(f"{'/'.join(options)}: ")  # get periodicity option from the user
    prepared_option = prepare_string(option)  # prepare periodicity for check
    is_existing_option = prepared_option in option  # check if entered periodicity is valid
    # if entered periodicity is not of the allowed options then repeat the process, otherwise return prepared periodicity
    if not is_existing_option:
        print("Invalid option.")
        return get_option()
    else:
        return prepared_option


def get_list():
    """
    Gets all habits from the database optionally filtered by periodicity
    :return: formatted habit list (id and title)
    """
    option = get_option()  # get filter option from the user
    habits = get_habits(option)  # get all habits from the database with specified periodicity
    result = ""
    # iterate over all retrieved habits and format result in format 'habit id, title'
    for item in habits:
        habit_id = item[0]
        title = item[1]
        result += f"id: {habit_id}, title: {title}\n"
    print(result)


def get_longest_streak_all():
    """
    Gets the longest streak among all habits
    :return: formatted the longest streak
    """
    response = requests.get(f'{URL}/streak')  # send request
    data = response.json()  # get JSON data from response
    longest_streak = data.get('longest_streak')  # get the longest streak (represented as list of lists containing row data)
    result = ""
    # format result
    for item in longest_streak:
        value = item[0]
        result += f"Longest streak: {value}"
    print(result)


def get_longest_streak_id():
    """
    Gets the longest streak of specified habit
    :return: formatted the longest streak
    """
    habit_id = get_id()  # get habit id from the user
    habits = get_habits()  # get all habits in the database
    is_existing_id = check_existing_id(habits, habit_id)  # check if received id exists in the database
    # if id exists then send request, get JSON data from response and format result, otherwise print error message
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
    """
    Gets command number from the user and calls the corresponding handler
    :return: message to the user
    """
    prompt_text = ("1 - return a list of currently tracked habits\n"
                   "2 - return the longest run streak of all defined habits\n"
                   "3 - return the longest run streak for a given habit\n"
                   "Enter option number: ")
    command_number = input(prompt_text)  # get command number from the user
    is_number = check_is_number(command_number)  # check if input can be converted to an integer
    # if input can be converted to an integer and is one of the possible options then call corresponding handler,
    # otherwise repeat the process
    if is_number and command_number in commands.keys():
        command_handler = commands.get(command_number)
        command_handler()
    else:
        print('Invalid option number.')
        get_habit_info()


# a dictionary of all available command options as keys and corresponding handlers as values
commands = {
    '1': get_list,
    '2': get_longest_streak_all,
    '3': get_longest_streak_id
}
