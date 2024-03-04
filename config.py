DB_NAME = 'habit.db'
PORT = 8000
URL = f'http://localhost:{PORT}'

periodicities = ['hourly', 'daily', 'weekly']
update_properties = ['title', 'periodicity', 'both']

create_schema = {
    'required': ['title', 'periodicity'],
    'properties': {
        'title': {'type': 'string', 'minLength': 1},
        'periodicity': {'type': 'string', 'enum': periodicities},
    }
}

update_schema = {
    'properties': {
        'title': {'type': 'string', 'minLength': 1},
        'periodicity': {'type': 'string', 'enum': periodicities},
    }
}


class Habit:
    def __init__(self, title='', periodicity=''):
        self.title = title
        self.periodicity = periodicity
