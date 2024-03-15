import unittest
import sqlite3
import queries
from datetime import datetime
from Habit import Habit
from common import DATETIME_FORMAT

now = datetime.now().strftime(DATETIME_FORMAT)


class TestHabitDatabase(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()
        self.cursor.execute(queries.setup)
        habit = Habit('test1', 'hourly')
        parameters = (
            habit.title,
            habit.periodicity,
            habit.creation_date,
            habit.completion_dates,
            habit.current_streak,
            habit.longest_streak
        )
        self.cursor.execute(queries.create, parameters)
        self.connection.commit()

    def test_create(self):
        habit = Habit('test2', 'daily')
        parameters = (
            habit.title,
            habit.periodicity,
            habit.creation_date,
            habit.completion_dates,
            habit.current_streak,
            habit.longest_streak
        )
        self.cursor.execute(queries.create, parameters)
        self.connection.commit()
        self.cursor.execute("SELECT COUNT(*) FROM Habit WHERE title=?", (habit.title,))
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 1)
        self.cursor.execute("SELECT COUNT(*) FROM Habit")
        count_all = self.cursor.fetchone()[0]
        self.assertEqual(count_all, 2)

    def test_check(self):
        habit = Habit(completion_dates=now)
        parameters = (habit.completion_dates, 1)
        self.cursor.execute(queries.check, parameters)
        self.connection.commit()
        self.cursor.execute("SELECT completion_dates FROM Habit WHERE id=1")
        completion_dates = self.cursor.fetchone()[0]
        self.assertEqual(completion_dates, now)

    def test_refresh_streak(self):
        habit = Habit(current_streak=1, longest_streak=2)
        parameters = (habit.current_streak, habit.longest_streak, 1)
        self.cursor.execute(queries.refresh_streak, parameters)
        self.connection.commit()
        self.cursor.execute("SELECT current_streak, longest_streak FROM Habit WHERE id=1")
        streaks = self.cursor.fetchone()
        self.assertEqual(streaks, (1, 2))

    def test_delete(self):
        self.cursor.execute(queries.delete, (1,))
        self.connection.commit()
        self.cursor.execute("SELECT COUNT(*) FROM Habit WHERE id=1")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 0)

    def test_update(self):
        habit = Habit(title='new title', periodicity='weekly')
        parameters = (habit.title, habit.periodicity, 1)
        self.cursor.execute(queries.update, parameters)
        self.connection.commit()
        self.cursor.execute("SELECT title, periodicity FROM Habit WHERE id=1")
        db_habit = self.cursor.fetchone()
        self.assertEqual(db_habit, ('new title', 'weekly'))

    def test_get_habit(self):
        self.cursor.execute(queries.get_habit, (1,))
        db_habit = self.cursor.fetchone()
        self.assertIsNotNone(db_habit)
        self.assertEqual(db_habit, (1, 'test1', 'hourly', now, '', 0, 0))

    def test_get_habits(self):
        periodicity = 'hourly'
        habit = Habit('test2', 'daily')
        parameters = (
            habit.title,
            habit.periodicity,
            habit.creation_date,
            habit.completion_dates,
            habit.current_streak,
            habit.longest_streak
        )
        self.cursor.execute(queries.create, parameters)
        self.connection.commit()
        self.cursor.execute(queries.get_habits, (periodicity, periodicity))
        db_habits = self.cursor.fetchall()
        self.assertEqual(len(db_habits), 1)
        periodicity = 'all'
        self.cursor.execute(queries.get_habits, (periodicity, periodicity))
        db_habits = self.cursor.fetchall()
        self.assertEqual(len(db_habits), 2)

    def test_get_longest_streak_all(self):
        habit = Habit('test2', 'daily', longest_streak=10)
        parameters = (
            habit.title,
            habit.periodicity,
            habit.creation_date,
            habit.completion_dates,
            habit.current_streak,
            habit.longest_streak
        )
        self.cursor.execute(queries.create, parameters)
        self.connection.commit()
        self.cursor.execute(queries.get_longest_streak_all)
        longest_streak = self.cursor.fetchone()[0]
        self.assertEqual(longest_streak, 10)

    def tearDown(self):
        self.connection.close()


if __name__ == '__main__':
    unittest.main()
