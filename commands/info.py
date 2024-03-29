import db
from Habit import Habit
from common import periodicities
from common import check_is_number, prepare_string, get_id


def get_option():
    """
    Function to get periodicity option (for optional filtering) from the user and check if it is one of the possible values
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
    Function to get all habits from the database optionally filtered by periodicity
    :return: formatted habit list (id and title)
    """
    option = get_option()  # get filter option from the user
    db_habits = db.get_habits((option, option))  # get all habits from the database with specified periodicity
    result = ""
    # iterate over all retrieved habits and format result in format 'habit id, title'
    for item in db_habits:
        habit_id = item[0]
        title = item[1]
        result += f"id: {habit_id}, title: {title}\n"
    print(result) if result else print('No habits found.')


def get_longest_streak_all():
    """
    Function to get the longest streak among all habits
    :return: formatted longest streak
    """
    longest_streak = db.get_longest_streak_all()  # get the longest streak (represented as list of lists containing row data)
    print(f"Longest streak: {longest_streak[0]}")


def get_longest_streak_id():
    """
    Function to get the longest streak of specified habit
    :return: formatted longest streak
    """
    habit_id = get_id()  # get habit id from the user
    query_parameters = (habit_id,)
    db_habit = db.get_habit(query_parameters)
    # if id exists then send request, get JSON data from response and format result, otherwise print error message
    if db_habit:
        habit = Habit(longest_streak=db_habit[6])
        longest_streak = habit.get_longest_streak()  # get the longest streak (represented as list of lists containing row data)
        print(f"Longest streak: {longest_streak}")
    else:
        print("Habit id does not exist.")
        get_longest_streak_id()


def get_habit_info():
    """
    Function to get command number from the user and call the corresponding handler
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
