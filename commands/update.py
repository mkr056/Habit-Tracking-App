import db
import common
from Habit import Habit


def update_title(habit, habit_id):
    """
    Function to update the title of the habit based on user input
    :param habit_id: id of the habit to update
    :param habit: habit
    :return: message to the user
    """
    new_title = common.get_title()  # get new habit title from the user
    habit.title = new_title
    habit.update(habit_id)
    print('Habit updated!')


#
#
def update_periodicity(habit, habit_id):
    """
    Function to update the periodicity of the habit based on user input
    :param habit_id: id of the habit to update
    :param habit: habit
    :return: message to the user
    """
    new_periodicity = common.get_periodicity()  # get new habit periodicity from the user
    habit.periodicity = new_periodicity
    habit.update(habit_id)
    print('Habit updated!')


def update_both(habit, habit_id):
    """
    Function to update the title and periodicity of the habit based on user input
    :param habit_id: id of the habit to update
    :param habit: habit
    :return: message to the user
    """
    new_title = common.get_title()  # get new habit title from the user
    new_periodicity = common.get_periodicity()  # get new habit periodicity from the user
    habit.title = new_title
    habit.periodicity = new_periodicity
    habit.update(habit_id)
    print('Habit updated!')


def get_property_name():
    """
    Function to get option (property) regarding habit update from the user
    :return: option (property) entered by the user
    """
    update_properties = properties.keys()  # list of all possible options (properties)
    property_name = input(f"Property name ({'/'.join(update_properties)}): ")  # get property name from the user
    prepared_property_name = common.prepare_string(property_name)  # prepare property for check
    is_existing_property_name = prepared_property_name in update_properties  # check if entered property is valid
    # if entered property is not of the allowed options then repeat the process, otherwise return prepared property
    if not is_existing_property_name:
        print("Invalid property name.")
        return get_property_name()
    else:
        return prepared_property_name


def update_habit():
    """
    Function to update habit properties in the database (triggered when update command is received)
    :return: message to the user
    """
    habit_id = common.get_id()  # get habit id from the user
    db_habit = db.get_habit((habit_id,))
    if db_habit:
        habit = Habit(
            db_habit[1],
            db_habit[2],
        )
        property_name = get_property_name()
        property_handler = properties.get(property_name)
        property_handler(habit, habit_id)
    else:
        print("Habit id does not exist.")
        update_habit()


# dictionary of all available options for updating a habit as keys and corresponding handlers as values
properties = {
    'title': update_title,
    'periodicity': update_periodicity,
    'both': update_both
}
