import json
import logging
import os
import signal
import sqlite3

from flask import Flask, request, jsonify
from flask_json_schema import JsonSchema, JsonValidationError

import helpers
import queries
from commands.check import check_habit
from commands.create import create_habit
from commands.delete import delete_habit
from commands.info import get_habit_info
from commands.update import update_habit
from common import create_schema, update_schema
from config import *

app = Flask(__name__)
logging.getLogger("werkzeug").disabled = True  # disables log info
schema = JsonSchema(app)


@app.errorhandler(JsonValidationError)
def validation_error(e):
    """
    Handler when an error occurs while validating against json schema
    :param e: Error
    :return: JSON
    """
    return jsonify({'error': e.message, 'errors': [validation_error.message for validation_error in e.errors]})


@app.route('/')
def prompt_user():
    """
    Connect to database -> execute setup sql queries -> execute application processes
    :return: JSON with status code
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.create)
    cursor.execute(queries.create_trigger)
    cursor.execute(queries.insert_predefined_habits)
    connection.commit()
    connection.close()
    while True:
        command = input("Enter a command (create/check/update/delete/info/exit): ")
        prepared_command = helpers.prepare_string(command)
        command_handler = commands.get(prepared_command)  # get function based on key (command)
        # if function exists then call it, otherwise print message and start new loop iteration
        if command_handler:
            command_handler()
        else:
            print("Invalid command.")
            continue
        if prepared_command == 'exit':  # if exit command is received then exit the infinite loop
            break
    return jsonify({'success': True}), 200


@app.route('/create', methods=['POST'])
@schema.validate(create_schema)  # validate against json schema
def create():
    """
    Crates a new habit in the database
    :return: JSON with status code
    """
    data = request.get_json()
    habit_data = json.loads(data)
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.insert, (habit_data['title'], habit_data['periodicity']))
    connection.commit()
    connection.close()
    return jsonify({'success': True}), 200


@app.route('/<habit_id>/update', methods=['POST'])
@schema.validate(update_schema)  # validate against json schema
def update(habit_id):
    """
    Updates a habit in the database (either habit name, periodicity or both) based on its id
    :param habit_id: is received from the url
    :return: JSON with status code
    """
    data = request.get_json()
    habit_data = json.loads(data)
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.update, (habit_data.get('title'), habit_data.get('periodicity'), habit_id))
    connection.commit()
    connection.close()
    return jsonify({'success': True}), 200


@app.route('/<habit_id>/delete', methods=['POST'])
def delete(habit_id):
    """
    Deletes a habit from the database based on its id
    :param habit_id: is received from the url
    :return: JSON with status code
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.delete, habit_id)
    connection.commit()
    connection.close()
    return jsonify({'success': True}), 200


@app.route('/<habit_id>/check', methods=['POST'])
def check(habit_id):
    """
    Checks/completes habit in the database based on its id
    :param habit_id: is received from the url
    :return: JSON with status code
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.check, habit_id)
    connection.commit()
    connection.close()
    return jsonify({'success': True}), 200


@app.route('/habits', methods=['GET'])
def get_habits():
    """
    Gets all habits from the database with optional filter based on periodicity received from query parameters
    :return: habits represented as JSON with status code
    """
    periodicity = request.args.get('periodicity')
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.validate_streak)
    cursor.execute(queries.get_habits, [periodicity, periodicity])
    habits = cursor.fetchall()
    connection.commit()
    connection.close()
    return jsonify({'habits': habits}), 200


@app.route('/streak', methods=['GET'])
def get_longest_streak():
    """
    Gets the longest streak either among all habits or for individual habit based on id received from query parameters
    :return: longest streak response as JSON with status code
    """
    habit_id = request.args.get('id')
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.validate_streak)
    # if habit id was found in query parameters then get habit's longest streak, otherwise get the longest among all habits
    if habit_id:
        cursor.execute(queries.get_longest_streak_id, habit_id)
    else:
        cursor.execute(queries.get_longest_streak_all)
    longest_streak = cursor.fetchall()
    connection.commit()
    connection.close()
    return jsonify({'longest_streak': longest_streak}), 200


def handle_exit():
    """
    Sends an interrupt signal to the current Python process (is called when exit command is received)
    """
    os.kill(os.getpid(), signal.SIGINT)
    print("Application has been terminated.")


# a dictionary of all available commands as keys and corresponding handlers as values
commands = {
    'create': create_habit,
    'update': update_habit,
    'delete': delete_habit,
    'check': check_habit,
    'info': get_habit_info,
    'exit': handle_exit
}

if __name__ == '__main__':
    app.run(port=PORT, debug=True)  # start the development server
