### Installation instructions:
1. Clone this repository: navigate to desired directory and run **git clone https://github.com/mkr056/Habit-Tracking-App.git**
2. Make sure Python version 3.7 or later is installed on your machine, otherwise download it: **https://www.python.org/downloads/**

### Run instructions (Application):
1. Open Terminal (Command Prompt) and navigate to the project folder
2. Run Python script (application): **python main.py**

### Run instructions (Tests):
1. Open Terminal (Command Prompt) and navigate to the project folder
2. Run Python script (tests): **python -m unittest test.py**

### Usage instructions:
To use this Habit Tracking application, follow these instructions:

#### Creating a new habit:
1. Type _**create**_ to begin.
2. Enter the title of your habit.
3. Specify how often you want to track this habit.

#### Checking off a habit:
1. Use _**check**_ followed by the habit's ID to mark it as completed.

#### Updating a habit's title:
1. Start with _**update**_ and provide the habit's ID.
2. Type _**title**_ and then enter the new title for the habit.

#### Updating a habit's periodicity:
1. Similarly, use _**update**_ and the habit's ID.
2. Type _**periodicity**_ and specify the new tracking frequency.

#### Updating both title and periodicity:
1. Enter _**update**_ with the _**both**_ command and provide the new title and periodicity.

#### Deleting a habit:
1. Type _**delete**_ followed by the habit's ID to remove it.

#### Viewing habits:
1. To see all tracked habits, type _**info**_, then _**1**_, and finally the _**all**_ command.
2. To view habits with a specific periodicity, use _**info**_, then _**1**_, and provide the periodicity filter.

#### Tracking streaks:
1. Check the longest streak of all habits with _**info**_ and then _**2**_.
2. Find the longest streak for a specific habit by using _**info**_, then _**3**_, and lastly specify the habit ID.

#### Exiting the application:
1. Simply type _**exit**_ to close the application.
