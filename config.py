DB_NAME = 'habit.db'
PORT = 8000
URL = f'http://localhost:{PORT}'

periodicities = ['hourly', 'daily', 'weekly']

habit_schema = {
    'required': ['title', 'periodicity'],
    'properties': {
        'title': {'type': 'string', 'minLength': 1},
        'periodicity': {'type': 'string', 'enum': periodicities},
    }
}
