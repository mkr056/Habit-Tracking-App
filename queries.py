from common import periodicities

periodicity_check = "CHECK(periodicity IN (" + ", ".join(["'{}'".format(periodicity) for periodicity in periodicities]) + "))"

create = f'''
    CREATE TABLE IF NOT EXISTS Habit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        periodicity TEXT NOT NULL {periodicity_check},
        creation_date TEXT DEFAULT CURRENT_TIMESTAMP,
        completion_dates TEXT,
        latest_completion TEXT,
        current_streak INTEGER NOT NULL DEFAULT 0,
        longest_streak INTEGER NOT NULL DEFAULT 0
    )
'''

insert = 'INSERT INTO Habit (title, periodicity) VALUES (?, ?)'

insert_predefined_habits = '''
    INSERT INTO Habit (title, periodicity) VALUES 
    ('test1', 'hourly'), 
    ('test2', 'daily'), 
    ('test3', 'weekly'),
    ('test4', 'hourly'),
    ('test5', 'daily')
'''

check = '''
    UPDATE Habit SET completion_dates = COALESCE(completion_dates || '\n', '') || datetime('now'), current_streak = CASE
        WHEN periodicity = 'hourly' AND (strftime('%s', 'now') - strftime('%s', latest_completion) <= 3600 OR latest_completion IS NULL) THEN current_streak + 1
        WHEN periodicity = 'daily' AND (strftime('%s', 'now') - strftime('%s', latest_completion) <= 86400 OR latest_completion IS NULL) THEN current_streak + 1
        WHEN periodicity = 'weekly' AND (strftime('%s', 'now') - strftime('%s', latest_completion) <= 604800 OR latest_completion IS NULL) THEN current_streak + 1
        ELSE 0
        END, latest_completion = datetime('now') WHERE id = ?;
'''

delete = 'DELETE FROM Habit WHERE id = ?'

update = '''
    UPDATE Habit SET title = COALESCE(?, title), periodicity = COALESCE(?, periodicity) WHERE id = ?
'''

get_habits = '''
    SELECT * FROM Habit WHERE periodicity = (CASE WHEN ? ="all" THEN periodicity ELSE ? END) ORDER BY id
'''

get_longest_streak_all = 'SELECT MAX(longest_streak) AS longest_streak FROM Habit'
get_longest_streak_id = 'SELECT longest_streak FROM Habit WHERE id = ?'

create_trigger = '''
    CREATE TRIGGER IF NOT EXISTS update_longest_streak AFTER UPDATE ON Habit
    BEGIN
     UPDATE Habit SET longest_streak = MAX(longest_streak, current_streak);
    END
'''

validate_streak = '''
    UPDATE Habit SET current_streak = CASE
        WHEN periodicity = 'hourly' AND (strftime('%s', 'now') - strftime('%s', latest_completion) <= 3600 OR latest_completion IS NULL) THEN current_streak
        WHEN periodicity = 'daily' AND (strftime('%s', 'now') - strftime('%s', latest_completion) <= 86400 OR latest_completion IS NULL) THEN current_streak
        WHEN periodicity = 'weekly' AND (strftime('%s', 'now') - strftime('%s', latest_completion) <= 604800 OR latest_completion IS NULL) THEN current_streak
        ELSE 0
        END;
'''