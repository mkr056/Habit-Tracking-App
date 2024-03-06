import requests
from config import URL
from common import periodicities


def prepare_string(string):
    """
    Removes leading and trailing spaces from a string and lowercases it
    :param string: text to be prepared
    :return: prepared string
    """
    return string.strip().lower()


def check_is_number(string):
    """
    Tries to convert string to integer
    :param string: number to be converted to integer
    :return: true if string can be converted to integer, false otherwise
    """
    try:
        int(string)
        return True
    except ValueError:
        return False


def check_existing_id(habits, habit_id):
    """
    Checks if given habit id exists in the database
    :param habits: list of all habits in database (represented as list of lists containing row data)
    :param habit_id: id to be checked
    :return: true if habit id is found, false otherwise
    """
    return any(sublist[0] == habit_id for sublist in habits)


def get_title():
    """
    Gets habit title from user and removes leading and trailing spaces with check for emptiness
    :return: title entered by the user
    """
    new_title = input("Enter title: ")
    stripped_title = new_title.strip()
    # if title is empty repeat the process, otherwise return trimmed title
    if not stripped_title:
        print("Invalid habit title.")
        return get_title()
    else:
        return stripped_title


def get_periodicity():
    """
    Gets habit periodicity from user with preparing and checks if it is one of the possible values
    :return: periodicity entered by the user as prepared string
    """
    periodicity = input(f"Habit periodicity ({'/'.join(periodicities)}): ")
    prepared_periodicity = prepare_string(periodicity)
    is_existing_periodicity = prepared_periodicity in periodicities
    # if entered periodicity is not of the allowed options then repeat the process, otherwise return prepared periodicity
    if not is_existing_periodicity:
        print("Invalid habit periodicity.")
        return get_periodicity()
    else:
        return prepared_periodicity


def get_id():
    """
    Gets habit id from the user and checks if it can be converted to number
    :return: habit id as integer
    """
    habit_id = input("Habit id: ")
    is_number = check_is_number(habit_id)
    # if entered number can't be converted to integer then repeat the process, otherwise return id as integer
    if not is_number:
        print("Invalid habit id.")
        return get_id()
    else:
        return int(habit_id)


def get_habits(periodicity='all'):
    """
    Gets all habits from the database optionally filtered by periodicity (send request and get json from response)
    :param periodicity: hourly/daily/weekly/all, all is default
    :return: list of habits
    """
    response = requests.get(f'{URL}/habits?periodicity={periodicity}')
    data = response.json()
    return data.get('habits')
