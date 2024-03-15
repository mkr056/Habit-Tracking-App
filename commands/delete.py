import db
from common import get_id


def delete_habit():
    """
    Function to delete habit from the database (triggered when delete command is received)
    :return: message to the user
    """
    habit_id = get_id()  # get habit id from the user
    query_parameter = (habit_id,)
    db_habit = db.get_habit(query_parameter)
    # if id exists then send request and print success message, otherwise print error message
    if db_habit:
        db.delete_habit(query_parameter)
        print('Habit deleted!')
    else:
        print("Habit id does not exist.")
        delete_habit()
