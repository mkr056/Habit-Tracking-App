from common import periodicities

periodicity_check = "CHECK(periodicity IN (" + ", ".join(["'{}'".format(periodicity) for periodicity in periodicities]) + "))"

setup = f'''
    CREATE TABLE IF NOT EXISTS Habit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        periodicity TEXT NOT NULL {periodicity_check},
        creation_date TEXT NOT NULL,
        completion_dates TEXT,
        current_streak INTEGER NOT NULL,
        longest_streak INTEGER NOT NULL
    )
'''

create = '''
    INSERT INTO Habit (title, periodicity, creation_date, completion_dates, current_streak, longest_streak) VALUES (?, ?, ?, ?, ?, ?)
'''

check = 'UPDATE Habit SET completion_dates = ? WHERE id = ?'

refresh_streak = 'UPDATE Habit SET current_streak = ?, longest_streak = ? WHERE id = ?'

delete = 'DELETE FROM Habit WHERE id = ?'

update = 'UPDATE Habit SET title = ?, periodicity = ? WHERE id = ?'

get_habit = 'SELECT * FROM Habit WHERE id = ?'

get_habits = '''
    SELECT * FROM Habit WHERE periodicity = (CASE WHEN ? ="all" THEN periodicity ELSE ? END) ORDER BY id
'''

get_longest_streak_all = 'SELECT MAX(longest_streak) AS longest_streak FROM Habit'