### Installation instructions:
1. Clone this repository: navigate to desired directory and run **git clone https://github.com/mkr056/Habit-Tracking-App.git**
2. Make sure Python version 3.7 or later is installed on your machine, otherwise download it: **https://www.python.org/downloads/**
3. Open Terminal (Command Prompt) and navigate to the project folder
4. Install external Python packages: **pip install -r packages.txt**
5. Close Terminal (Command Prompt) window

### Run instructions:
1. Open 2 Terminal (Command Prompt) windows
2. Inside the first window:
   1. navigate to the project folder
   2. Make sure that port 8000 is not in use already, otherwise change in project config (**config.py**)
   3. run Python script: **python main.py**
3. Inside the second window:
   1. send request to the root endpoint: **curl "http://localhost:8000/"** (if port is unchanged)
4. Verify that application has launched inside the first window

### Usage instructions (continuation...):
IMPORTANT NOTE: all commands surrounded with brackets (<>) refer to user input (not actual wording)!
- Commands for **Creating a habit**:
  1. create
  2. <habit_title>
  3. <habit_periodicity>
- Commands for **Checking a habit**:
  1. check
  2. <habit_id>
- Commands for **Updating a habit's title**
  1. update
  2. <habit_id>
  3. title
  4. <habit_title>
- Commands for **Updating a habit's periodicity**
  1. update
  2. <habit_id>
  3. periodicity
  4. <habit_periodicity>
- Commands for **Updating a habit's title and periodicity**
  1. update
  2. <habit_id>
  3. both
  4. <habit_title>
  5. <habit_periodicity>
- Commands for **Deleting a habit**
  1. delete
  2. <habit_id>
- Commands for **Returning a list of all currently tracked habits**
  1. info
  2. 1
  3. all
- Commands for **Returning a list of all habits with the same periodicity**
  1. info
  2. 1
  3. <habit_periodicity>
- Commands for **Returning the longest run streak of all defined habits**
  1. info
  2. 2
- Commands for **Returning the longest run streak for a given habit**
  1. info
  2. 3
  3. <habit_id>
- Commands for **Terminating the application**
  1. exit
