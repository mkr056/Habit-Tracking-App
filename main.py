import sqlite3
import json, os, signal
# import logging
from flask import Flask, request, jsonify
from flask_json_schema import JsonSchema, JsonValidationError
import helpers
from commands.create import create_habit
from commands.update import update_habit
from commands.check import check_habit
from commands.delete import delete_habit
from commands.info import get_habit_info
from config import *
from common import create_schema, update_schema
import queries

app = Flask(__name__)
# logging.getLogger("werkzeug").disabled = True
schema = JsonSchema(app)


@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({'error': e.message, 'errors': [validation_error.message for validation_error in e.errors]})


@app.route('/')
def prompt_user():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.create)
    cursor.execute(queries.create_trigger)
    connection.commit()
    connection.close()
    while True:
        command = input("Enter a command (create/check/update/delete/info/exit): ")
        prepared_command = helpers.prepare_string(command)
        command_handler = commands.get(prepared_command, handle_invalid_input)
        command_handler()
        if prepared_command == 'exit':
            break
    return jsonify({'success': True}), 200


@app.route('/create', methods=['POST'])
@schema.validate(create_schema)
def create():
    data = request.get_json()
    habit_data = json.loads(data)
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.insert, (habit_data['title'], habit_data['periodicity']))
    connection.commit()
    connection.close()
    return jsonify({'success': True}), 200


@app.route('/<habit_id>/update', methods=['POST'])
@schema.validate(update_schema)
def update(habit_id):
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
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.delete, habit_id)
    connection.commit()
    connection.close()
    return jsonify({'success': True}), 200


@app.route('/<habit_id>/check', methods=['POST'])
def check(habit_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.check, habit_id)
    connection.commit()
    connection.close()
    return jsonify({'success': True}), 200


@app.route('/habits', methods=['GET'])
def get_habits():
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
    habit_id = request.args.get('id')
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.validate_streak)
    if habit_id:
        cursor.execute(queries.get_longest_streak_id, habit_id)
    else:
        cursor.execute(queries.get_longest_streak_all)
    longest_streak = cursor.fetchall()
    connection.commit()
    connection.close()
    return jsonify({'longest_streak': longest_streak}), 200


def handle_exit():
    os.kill(os.getpid(), signal.SIGINT)
    print("Application has been terminated.")


def handle_invalid_input():
    print("Invalid command.")
    return prompt_user()


commands = {
    'create': create_habit,
    'update': update_habit,
    'delete': delete_habit,
    'check': check_habit,
    'info': get_habit_info,
    'exit': handle_exit
}

if __name__ == '__main__':
    app.run(port=PORT, debug=True)
