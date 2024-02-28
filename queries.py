from config import periodicities

periodicity_check = "CHECK(periodicity IN (" + ", ".join(["'{}'".format(p) for p in periodicities]) + "))"

create = f'''
        CREATE TABLE IF NOT EXISTS Habit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            periodicity TEXT NOT NULL {periodicity_check},
            creation_date TEXT DEFAULT CURRENT_TIMESTAMP,
            completion_dates TEXT,
            current_streak INTEGER NOT NULL DEFAULT 0,
            longest_streak INTEGER NOT NULL DEFAULT 0
        )
    '''

insert = 'INSERT INTO Habit (title, periodicity) VALUES (?, ?)'