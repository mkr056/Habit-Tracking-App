import sqlite3
import json
# import logging
from flask import Flask, request, jsonify
from flask_json_schema import JsonSchema, JsonValidationError
import helpers
from create import create_habit
from update import update_habit
from check import check_habit
from delete import delete_habit
from config import *
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
    connection.commit()
    connection.close()
    command = input("Enter a command (create/check/update/delete/info/exit): ")
    prepared_command = helpers.prepare_string(command)
    command_handler = commands.get(prepared_command, handle_invalid_input)
    command_handler()
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
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(queries.get_habits)
    habits = cursor.fetchall()
    connection.commit()
    connection.close()
    return jsonify({'habits': habits}), 200


def handle_invalid_input():
    print("Invalid command.")
    return prompt_user()


commands = {
    'create': create_habit,
    'update': update_habit,
    'delete': delete_habit,
    'check': check_habit,
}

if __name__ == '__main__':
    app.run(port=PORT, debug=True)
