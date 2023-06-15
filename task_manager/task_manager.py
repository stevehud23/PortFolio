                            #  Task manager program
'''
this program creates user tasks, generates reports, displays stats, creates new users, and even has a random password generator 
and is complete with error checks to ensure the program wont crash
'''
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as file:
        pass

# Read task data from tasks.txt
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

# Convert task data to a list of dictionaries
task_list = []
for t_str in task_data:
    curr_t = {}
    task_components = t_str.split(";")
    if len(task_components) == 6:
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        try:
            curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
            curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        except ValueError:
            print(f"Invalid date format in task: {t_str}")
            continue
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)
    else:
        print(f"Invalid task format: {t_str}")

# Read user data from user.txt
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert user data to a dictionary
username_password = {}
for user in user_data:
    if user:
        user_components = user.split(';')
        if len(user_components) == 2:
            username, password = user_components
            username_password[username] = password
        else:
            print(f"Invalid user format: {user}")


# create generate report function

from datetime import datetime
import time

def gen_report(curr_user):
    # Check if the current user is admin
    if curr_user != "admin":
        print("\nAccess Denied: Only the admin user can generate reports.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current date and time

    if not os.path.exists("task_overview.txt"):  # Create task_overview.txt file
        with open("task_overview.txt", "w") as gen_file:
            pass

    if not os.path.exists("user_overview.txt"):  # Create user_overview.txt file
        with open("user_overview.txt", "w") as user_file:
            pass

    # sets Count for number of completed, uncompleted, and overdue tasks
    completed_count = 0
    uncompleted_count = 0
    overdue_count = 0

    '''
    initialises the three variables and iterates each task in task list with keys given 
    checks value of the key 'completed' and sets the value to true if found completed_count +1
    otherwise sets uncompleted_count +1
    due_date' key) is earlier than the current date (obtained using datetime.now().date()), increments the overdue_count variable by 1. 
    This allows tracking the count of overdue tasks
    '''     
    for task in task_list:
        if task['completed']:
            completed_count += 1  
        else:
            uncompleted_count += 1
            if task['due_date'].date() < datetime.now().date():
                overdue_count += 1
    total_tasks = len(task_list)
    incomplete_count = uncompleted_count - overdue_count

    try:
        # Calculate the percentages
        completed_percentage = (completed_count / total_tasks) * 100
        uncompleted_percentage = (uncompleted_count / total_tasks) * 100
        overdue_percentage = (overdue_count / total_tasks) * 100
        incomplete_percentage = (incomplete_count / total_tasks) * 100

        # Display the task overview
        with open("task_overview.txt", "w") as task_file:
            task_file.write(f"Task Overview (Generated on {timestamp})\n")
            task_file.write(f"Total tasks: {total_tasks}\n")
            task_file.write(f"Completed tasks: {completed_count} ({completed_percentage:.2f}%)\n")
            task_file.write(f"Uncompleted tasks: {uncompleted_count} ({uncompleted_percentage:.2f}%)\n")
            task_file.write(f"Overdue tasks: {overdue_count} ({overdue_percentage:.2f}%)\n")
            task_file.write(f"Incomplete tasks: {incomplete_count} ({incomplete_percentage:.2f}%)\n")

        # Count the tasks assigned to each user
        user_tasks = {}
        for task in task_list:
            username = task['username']
            if username in user_tasks:
                user_tasks[username] += 1
            else:
                user_tasks[username] = 1

        # Calculate the percentages for each user
        user_percentages = {}
        for username, task_count in user_tasks.items():
            user_percentages[username] = (task_count / total_tasks) * 100

        # Display the user overview
        with open("user_overview.txt", "w") as user_file:
            user_file.write(f"User Overview (Generated on {timestamp})\n")
            user_file.write(f"Total users: {len(username_password)}\n")
            user_file.write(f"Total tasks: {total_tasks}\n")
            user_file.write("\nTask distribution by user:\n")
            for username, task_count in user_tasks.items():
                user_file.write(f"{username}: {task_count} tasks ({user_percentages[username]:.2f}%)\n")

        print("\nReport generated.")

    # Zero division error check complete, prompt user the system found error as no data to parse for equation
    # take user to add task section to update 
    except ZeroDivisionError:
        time.sleep(1)
        print("\nError: Division by zero occurred. Please add a task.")
        time.sleep(2)
        print("\nTaking admin user to add task section\n")
        time.sleep(3)
        add_task()

    # Option to view user_overview.txt and task_overview.txt for admin user
    if curr_user == "admin":
        while True:
            choice = input("\nDo you want to view the generated reports? (Y/N): ").lower()
            if choice == 'y':
                try:
                    with open("user_overview.txt", "r") as user_file:
                        print("\n[user_overview.txt]")
                        print(user_file.read())

                    with open("task_overview.txt", "r") as task_file:
                        print("\n[task_overview.txt]")
                        print(task_file.read())
                   
                except FileNotFoundError:
                    print("No reports found. Please generate the reports first.")
            elif choice == 'n':
                break
            else:
                print("Invalid choice. Please enter Y for Yes or N for No.")
    else:
        print("Report generated. Only admin user can view the reports.")

def view_mine(curr_user):

    '''Reads the tasks from tasks.txt file assigned to the current user
       and prints them to the console with corresponding menu options
    '''
    tasks_assigned = [t for t in task_list if t['username'] == curr_user]
    incomplete_tasks = [t for t in tasks_assigned if not t['completed']]
    total_tasks = len(incomplete_tasks)
    current_task_index = 0

    while current_task_index < total_tasks:
        task = incomplete_tasks[current_task_index]

        disp_str = f"Task: \t\t\t {task['title']}\n"
        disp_str += f"Assigned to: \t\t {task['username']}\n"
        disp_str += f"Date Assigned: \t\t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t\t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description:\t {task['description']}\n"

        print(f"\nTask {current_task_index+1} of {total_tasks}:")
        print(disp_str)

        # Check if task is completed
        if task['completed']:
            print("\nTask is already completed. No further action can be taken.")         
        else:
            # task options
            task_completed = False
            while not task_completed:
                menu_option = input('''Menu options: 
                (1) Edit task 
                (2) Complete task 
                (3) Next task 
                (-1) Back to menu
                please select from the options above:  ''').lower()

                # Edit / update task details
                # checks if task completed true or false 
                # display message if task is completed to prompt user that cant edit a completed task 
                if menu_option == '1':
                    if not task['completed']:
                        print("Editing task...")
                        task['title'] = input("Enter the updated title: ")
                        task['description'] = input("Enter the updated description: ")
                        task_due_date = input("Enter the updated due date (YYYY-MM-DD): ")
                        task['due_date'] = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                        print("Task details updated.")
                    else:
                        print("\nCannot edit a completed task.")
                    break
                elif menu_option == '2':                   
                    if not task['completed']:  # Mark task as completed
                        task['completed'] = True
                        print("\nTask marked as completed.")
                        task_completed = True  # Set the flag to indicate task completion
                        current_task_index += 1

                    else:
                        print("\nTask is already completed.")
                        task_completed = True  # Set the flag to indicate task completion
                    break
                elif menu_option == '3':
                    if current_task_index == total_tasks:
                        print("\nNo more tasks.")
                    else:
                        print("Cannot move to the next task until the current task is completed.\n")
                elif menu_option == '-1':
                    # Go back to the main menu
                    return
                else:
                    print("\nInvalid option. Please try again.")

        # Check if all tasks have been completed
        if current_task_index == total_tasks:
            print("\nAll tasks completed.")

    # If all tasks have been completed or if there are no tasks
    print("\nNo more tasks to display.")

    '''Reads the tasks from tasks.txt file and prints to the console in the 
       format of Output 2 presented in the task pdf (i.e. includes spacing
       and labelling) grants admin rights only
    '''
def view_all(curr_user):
    if curr_user == "admin":
        print("All tasks:\n")
        for t in task_list:
            disp_str = f"Task: \t\t\t {t['title']}\n"
            disp_str += f"Assigned to: \t\t {t['username']}\n"
            disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description:\t {t['description']}\n"
            print(disp_str)
    else:
        print("\nAccess denied. Only admin can view all tasks.")

def add_task():

    # Add task option, checks if user entered by user exsists, if user exsists then continue with rest of function
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("\nUser does not exist. Please enter a valid username\n")
        add_task()
        return
    
    # creation of new task title, creation of new task description 
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    # gets the due date of the task 
    # converts the entered date string into a datetime object parsed using .strptime(), and then breaks out of the loop
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("\nInvalid datetime format. Please use the format specified\n")

    # Get the current date.
    curr_date = date.today()

    # Add the data to the task list
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)

    # Write the updated task list to tasks.txt
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

    print("Task successfully added.")

import random
import string
import re

'''
this function evaluates and matches a specific pattern requirment for user input of username
^[a-zA-Z][a-zA-Z0-9]*$ ensures that the username starts with an alphabetic character and is followed by zero or more 
alphanumeric characters.This pattern allows usernames that consist of letters and digits but must start with a letter
''' 
def reg_user():
    while True:
        username = input("\nEnter new username: ")
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', username):
            print("\nInvalid username. Please enter a username with letters followed by numbers or letters only.")
        elif username in username_password:
            print("\nUsername already exists. Please enter a different username.")
        else:
            break

    
    # Error checks user input for random password generator
    while True:
        random_password = input("\nGenerate random password? (y/n): ").lower()
        if random_password == 'y':

            # initalises random password generator, max length 10.
            # create string variable called characters 
            # string.ascii_letters contains all upper/lower case ascii letters
            # string.digits represents all numbers 0-9
            # string.punctuation represents some common punctuation marks
            # random is repeatedly called to select and concatinate selected chars to form a random password
            password_length = 10
            characters = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(random.choice(characters) for _ in range(password_length))
            break
        elif random_password == 'n':
            password = input("\nEnter new password: ")
            break
        else:
            print("\nInvalid choice. Please enter 'y' or 'n'.")

    # write new username and password to user.txt, display confirmination message
    username_password[username] = password
    with open("user.txt", "a") as user_file:
        user_file.write(f"{username};{password}\n")
        print(f"\nnew user name : {username}\nnew password : {password}")
    print("\nUser registration successful!")

# Load existing username-password pairs from user.txt
username_password = {}
with open("user.txt", "r") as user_file:
    for line in user_file:
        line = line.strip()
        if line:
            values = line.split(";")
            if len(values) >= 2:
                username_password[values[0]] = values[1]

def login():
    logged_in = False        # condition preset to false
    curr_user = None         # current user is none as not logged in yet
    login_attempts = 0       # login count 
    forgot_password = False  # preset to False only True if user selects forgot password  

    # validates user login credentials, if both are found in dict then login successful.   
    while not logged_in:
        print("LOGIN:")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")

        if curr_user in username_password:
            if curr_pass == username_password[curr_user]:
                print("Login successful!")
                logged_in = True
                break
            else:

                # the logic of this part is to check the password validation 
                # sets a count for user to see how many tries  until program shutdown or password reset
                login_attempts += 1
                remaining_attempts = 3 - login_attempts
                print(f"\nInvalid password. {remaining_attempts} attempts remaining.")

                # if user has 1 attempt left display a warning message with an option to reset password
                # used defensive programming for user inputs
                if remaining_attempts == 1:
                    while True:
                        reset_choice = input("You have one attempt remaining. Forgot password? (Y/N): ")
                        if reset_choice.upper() == "Y":
                            forgot_password = True
                            reg_user()     # initalise register user function
                            break
                        elif reset_choice.upper() == "N":
                            print("\nIf you are having difficulties logging in please contact admin:")
                            break
                        else:
                            print("Invalid choice. Please enter 'Y' or 'N'.")

                # If user max tries, login option must be "Y" or exit program, or "N" manual quit
                if login_attempts >= 3:
                    while True:
                        reset_choice = input("\nYou have reached the maximum number of login attempts. Forgot password? (Y/N): ")
                        if reset_choice.upper() == "Y":
                            forgot_password = True
                            reg_user()  # Take user to reset password option
                            break
                        elif reset_choice.upper() == "N":
                            print("\nIf you are having difficulties logging in please contact admin:")
                            print("\n\nExiting Program....")
                            quit()
                        else:
                            print("Invalid choice. Please enter 'Y' or 'N'.")
        
        # the logic of this part is to check the user name validation 
        # sets a count for user to see how many tries until program shutdown or username reset
        else:
            login_attempts += 1
            remaining_attempts = 3 - login_attempts
            print(f"\nUsername not found. {remaining_attempts} attempts remaining.")

            # if user has 1 attempt left display a warning message with an option to reset password
            # used defensive programming for user inputs 
            if remaining_attempts == 1:
                while True:
                    reset_choice = input("\nYou have one attempt remaining. Forgot password? (Y/N): ")
                    if reset_choice.upper() == "Y":
                        forgot_password = True
                        reg_user()
                        break
                    elif reset_choice.upper() == "N":
                        print("\nIf you are having difficulties logging in please contact admin:")
                        break
                    else:
                        print("Invalid choice. Please enter 'Y' or 'N'.")

            # If user max tries, login option must be "Y" or exit program, or "N" manual quit
            if login_attempts >= 3:
                while True:
                    reset_choice = input("You have reached the maximum number of login attempts. Forgot password? (Y/N): ")
                    if reset_choice.upper() == "Y":
                        forgot_password = True    
                        reg_user()  # Take user to reset password option
                        break
                    elif reset_choice.upper() == "N":
                        print("\nIf you are having difficulties logging in please contact admin:")
                        print("\n\nExiting Program....")
                        quit()
                    else:
                        print("Invalid choice. Please enter 'Y' or 'N'.")

    return curr_user    # returns the current user value, this comes in handy later in the code 

# display user stats function with 1 positional argument to retrive current user
# function only accessed by admin
def display_stats(curr_user):
    if curr_user == "admin":
        # function can also only be initialized if a report has been generated
        if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
            print("No reports have been generated.")
            time.sleep(2)
            print("Taking Admin to main menu selection")
            time.sleep(3)
            return

        # print task/user overview.txt files using task/user_contents to display stats
        print("\nTask Overview:")
        with open("task_overview.txt", "r") as task_file:
            task_contents = task_file.read()
            if task_contents:
                print(task_contents)
            else:
                print("Task Overview is empty.")

        print("\nUser Overview:")
        with open("user_overview.txt", "r") as user_file:
            user_contents = user_file.read()
            if user_contents:
                print(user_contents)
            else:

                # prompt user file is empty, take user to report generator to update
                print("User Overview is empty.")
                print("\nAdmin must Generate a report first")
                time.sleep(2)
                print("Taking Admin to the report generator")
                time.sleep(3)
                gen_report(curr_user)
                
        #  menu options with defensive programming 
        print()
        while True:     
            option = input("\nSelect an option (p - Print, d - Delete, q - Quit): ").lower()
            if option == 'p':
                print("Printing files...")
                print()
                print("Task Overview:")
                print(task_contents)
                print("User Overview:")
                print(user_contents)
                break

            elif option == 'd':     # option to delete task/user.overview reports if found in operaintg system path
                print("\nDeleting files...")
                os.remove("task_overview.txt")
                os.remove("user_overview.txt")
                print("Files deleted successfully.")
                break
            elif option == 'q':    # option to exit current screen 
                print("\nReturning to menu.")
                break
            else:
                print("Invalid option. Please select a valid option.")
    else:
        print("\nAccess denied. Only admin can display statistics.")
    return

# user  menu options with functionality   
def menu_1():
    curr_user = login()  # Retrieve the current user from the login function
    while True:
        print()
        menu = input('''Select one of the following options below:
    r - Register a user
    a - Add a task
    va - View all tasks
    vm - View my tasks
    gr - Generate reports (over writes exsisting report if one has been created)
    ds - Display statistics
    u  - Switch user
    e - Exit
    : ''').lower()

        if menu == 'r':
            reg_user()                # Pass any user to reg_user function # all user's 
        elif menu == 'a':             
            add_task()                # Pass any user to add_task function # all user's
        elif menu == 'va':            
            view_all(curr_user)       # Pass the curr_user variable to the view_all function # viewable by admin only
        elif menu == 'vm':           
            view_mine(curr_user)      # Pass the curr_user variable to the view_mine function # all user's
        elif menu == 'gr':            
            gen_report(curr_user)     # Pass the curr_user variable to the gen_report function # viewable by admin only
        elif menu == 'ds':            
            display_stats(curr_user)  # Pass the curr_user variable to the display_stats function # viewable by admin only 
        elif menu == 'u':
            curr_user = login()       # pass curr_user variable to the login function # all user's
        elif menu == 'e':             
            break
        else:
            print("Invalid option. Please try again.")

menu_1()

#=====================================Time complexity Big O Notation=================================#
#                                                                                                    #
#  based on current code and inputs within:   O(n + m + k + p)                                       #  
#                                                                                                    #
#  dominant factors:      reading data from files (O(n)), converting task data to a list (O(m)),     #
#                         and generating a report (O(m)).                                            #
#                         The number of users is k. ' this can change'                               #
#                         The number of tasks assigned to the current user is p. 'this can change'   #
#====================================================================================================#