periodicities = ['hourly', 'daily', 'weekly']  # list of all possible periodicity options

# json schema for creating a habit (title and periodicity properties are required)
create_schema = {
    'required': ['title', 'periodicity'],
    'properties': {
        'title': {'type': 'string', 'minLength': 1},
        'periodicity': {'type': 'string', 'enum': periodicities},
    }
}

# json schema for updating a habit (title and periodicity properties are optional)
update_schema = {
    'properties': {
        'title': {'type': 'string', 'minLength': 1},
        'periodicity': {'type': 'string', 'enum': periodicities},
    }
}


# Habit class with title and periodicity fields
class Habit:
    def __init__(self, title='', periodicity=''):
        self.title = title
        self.periodicity = periodicity
