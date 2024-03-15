import db
from datetime import datetime
from common import DATETIME_FORMAT, time_difference


class Habit:
    def __init__(
            self,
            title='',
            periodicity='',
            creation_date=datetime.now().strftime(DATETIME_FORMAT),
            completion_dates='',
            current_streak=0,
            longest_streak=0):
        """
        Method to initialize a Habit object with default values or provided parameters
        :param title: title of the habit
        :param periodicity: periodicity of the habit
        :param creation_date: date when the habit was created
        :param completion_dates: dates on which the habit was completed
        :param current_streak: current streak of completing the habit
        :param longest_streak: longest streak of completing the habit
        """
        self.title = title
        self.periodicity = periodicity
        self.creation_date = creation_date
        self.completion_dates = completion_dates
        self.current_streak = current_streak
        self.longest_streak = longest_streak

    def create(self):
        """
        Method to create a new habit by adding it to the database with the specified parameters
        """
        parameters = (
            self.title,
            self.periodicity,
            self.creation_date,
            self.completion_dates,
            self.current_streak,
            self.longest_streak
        )
        db.create_habit(parameters)

    def check(self, habit_id):
        """
        Method to update the completion dates of an existing habit in the database
        :param habit_id: id of the habit in the database
        """
        now = datetime.now().strftime(DATETIME_FORMAT)
        if self.completion_dates:
            self.completion_dates = self.completion_dates + ',' + now
        else:
            self.completion_dates = now
        parameters = (
            self.completion_dates,
            habit_id
        )
        db.check_habit(parameters)

    def update(self, habit_id):
        """
        Method to update the title and/or periodicity of an existing habit in the database
        :param habit_id: id of the habit in the database
        """
        parameters = (
            self.title,
            self.periodicity,
            habit_id
        )
        db.update_habit(parameters)

    def refresh_streak(self, habit_id):
        """
        Method to calculate and update the current streak and longest streak of completing the habit
        :param habit_id: id of the habit in the database
        """
        # split completion dates if they exist, otherwise initialize as empty list
        if self.completion_dates:
            completion_dates = self.completion_dates.split(',')
        else:
            completion_dates = []

        # convert completion dates to datetime objects
        datetime_objects = [datetime.strptime(date_str, DATETIME_FORMAT) for date_str in completion_dates]

        current_streak = 0
        longest_streak = 0
        previous_date = None

        periodicity = self.periodicity

        # calculate current streak and longest streak based on completion dates
        for date in datetime_objects:
            # if it is the first timestamp in the list or if the difference between working timestamp
            # and previous timestamp is less than or equal to specified time difference,
            # then increase the current streak, otherwise make it equal to 1
            if not previous_date or date - previous_date <= time_difference[periodicity]:
                current_streak += 1
            else:
                current_streak = 1

            # update the longest streak if it is less than current streak
            if current_streak > longest_streak:
                longest_streak = current_streak

            previous_date = date

        self.current_streak = current_streak
        self.longest_streak = longest_streak
        parameters = (
            self.current_streak,
            self.longest_streak,
            habit_id
        )
        db.refresh_streak(parameters)

    def get_longest_streak(self):
        """
        Method to get the longest streak of completing the habit
        :return: the longest streak of completing the habit
        """
        return self.longest_streak
