import sqlite3
import queries

DB_NAME = 'habit.db'


def setup_table():
    """
    Function to create the habit table in the database if it doesn't exist
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.setup)
    connection.commit()
    connection.close()

def refresh_streak(parameters):
    """
    Function to update the streak information in the database for a specific habit
    :param parameters: list of parameters containing current streak, longest streak, and habit id.
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.refresh_streak, parameters)
    connection.commit()
    connection.close()


def create_habit(parameters):
    """
    Function to insert a new habit into the database
    :param parameters: list of parameters containing habit information
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.create, parameters)
    connection.commit()
    connection.close()


def check_habit(parameters):
    """
    Function to check (complete) a specific habit in the database
    :param parameters: list of parameters containing completion dates and habit id
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.check, parameters)
    connection.commit()
    connection.close()


def update_habit(parameters):
    """
    Function to update the title and/or periodicity information in the database for a specific habit
    :param parameters: list of parameters containing title, periodicity, and habit id
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.update, parameters)
    connection.commit()
    connection.close()


def delete_habit(parameters):
    """
    Function to delete a specific habit from the database
    :param parameters: list of parameters containing habit id
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.delete, parameters)
    connection.commit()
    connection.close()


def get_habit(parameters):
    """
    Function to retrieve a specific habit from the database
    :param parameters: list of parameters containing habit id
    :return: retrieved habit
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.get_habit, parameters)
    habit = cursor.fetchone()
    connection.commit()
    connection.close()
    return habit


def get_habits(parameters):
    """
    Function to retrieve all habits from the database optionally filtering based on periodicity
    :param parameters: list of parameters containing filtering option (hourly/daily/weekly/all)
    :return: retrieved habits
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.get_habits, parameters)
    habits = cursor.fetchall()
    connection.commit()
    connection.close()
    return habits


def get_longest_streak_all():
    """
    Function to retrieve the longest streak of all habits from the database
    :return: the longest streak across all habits
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.get_longest_streak_all)
    longest_streak = cursor.fetchone()
    connection.commit()
    connection.close()
    return longest_streak
