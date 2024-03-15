from datetime import timedelta

periodicities = ['hourly', 'daily', 'weekly']  # list of all possible periodicity options
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
time_difference = {  # dictionary of all available periodicities as keys and corresponding time differences as values
    "hourly": timedelta(hours=1),
    "daily": timedelta(days=1),
    "weekly": timedelta(weeks=1)
}


def prepare_string(string):
    """
    Function to remove leading and trailing spaces from a string and lowercase it
    :param string: text to be prepared
    :return: prepared string
    """
    return string.strip().lower()


def check_is_number(string):
    """
    Function that tries to convert string to integer
    :param string: number to be converted to integer
    :return: true if string can be converted to integer, false otherwise
    """
    try:
        int(string)
        return True
    except ValueError:
        return False


def get_title():
    """
    Function to get habit title from user and remove leading and trailing spaces with check for emptiness
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
    Function to get habit periodicity from user with preparing and check if it is one of the possible values
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
    Function to get habit id from the user and check if it can be converted to number
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
