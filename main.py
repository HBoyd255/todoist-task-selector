import random
import webbrowser
from todoist_api_python.api import TodoistAPI
import pickle


def text_file_to_string(file_path):
    """Reads the contents of a text file into a string.

    Args:
        file_path (Str): The file location of the text file.

    Returns:
        (Str): The contents of the text file.
    """
    with open(file_path, "r") as f:
        return f.read()


def save_object(object, pickle_path):
    """Saves an object to a pickle file.

    Args:
        object (Any): The object to be saved.
        pickle_path (Str): The file location to save the object.
    """

    with open(pickle_path, "wb") as f:
        pickle.dump(object, f)


def load_object(pickle_path):
    """Loads an object from a pickle file.

    Args:
        pickle_path (Str): The file location of the saved object.

    Returns:
        (Any): The loaded object.
    """
    with open(pickle_path, "rb") as f:
        return pickle.load(f)


def filter_tasks_by_label(label_name, tasks):
    """Filters tasks by a label name.

    Args:
        label_name (Str): The name of the label to filter by.
        tasks (List): A list of tasks.

    Returns:
        (List): A list of tasks that have the specified label.
    """

    # Create an empty list of tasks to return.
    tasks_to_return = []

    # Iterate through each task.
    for task in tasks:
        # If the label name is in the task's labels, add the task to the list.
        if label_name in task.labels:
            tasks_to_return.append(task)

    # Return the list of tasks.
    return tasks_to_return


# If set to True, the data will be loaded from the pickle files.
# If set to False, the data will be loaded from the Todoist API.
# This allows for faster testing.
LOAD_FROM_PICKLE = False

# The API key is stored in a text file to keep it secret from the git
# repository.
API_TEXT_FILE = "secrets/api_key.txt"
API_KEY = text_file_to_string(API_TEXT_FILE)

# Create an instance of the Todoist API.
api = TodoistAPI(API_KEY)


if LOAD_FROM_PICKLE:
    all_projects = load_object("secrets/projects.pickle")
    all_tasks = load_object("secrets/tasks.pickle")
    labels = load_object("secrets/labels.pickle")

else:
    all_projects = api.get_projects()
    all_tasks = api.get_tasks()
    labels = api.get_labels()

    save_object(all_projects, "secrets/projects.pickle")
    save_object(all_tasks, "secrets/tasks.pickle")
    save_object(labels, "secrets/labels.pickle")


label_names = [label.name for label in labels]


import tkinter as tk


def label_selected_screen(label):
    """Display the menu that details a random task from a chosen context."""

    # Clear the main window.
    for widget in root.winfo_children():
        widget.destroy()

    tasks_with_label = filter_tasks_by_label(label, all_tasks)

    task_count = len(tasks_with_label)

    task_count_label = tk.Label(
        root, text=f"There are {task_count} tasks", font=("Helvetica", 16)
    )
    task_count_label.pack(pady=20)

    back_button = tk.Button(root, text="Back", command=show_label_menu)

    back_button.pack(pady=20)

    if task_count == 0:
        return

    reroll_button = tk.Button(
        root,
        text="Reroll",
        command=lambda o=label: label_selected_screen(label),
    )
    reroll_button.pack(pady=20)

    random_task = random.choice(tasks_with_label)

    random_task_name = random_task.content
    random_task_url = random_task.url
    random_task_description = random_task.description

    print(random_task)

    task_name_label = tk.Label(
        root, text=f"Task: {random_task_name}", font=("Helvetica", 16)
    )

    task_name_label.pack(pady=20)

    if random_task_description:
        task_description_label = tk.Label(
            root,
            text=f"{random_task_description}",
            font=("Helvetica", 10),
        )
        task_description_label.pack(pady=20)

    view_online_button = tk.Button(
        root,
        text="View Online",
        command=lambda o=random_task_url: webbrowser.open(random_task_url),
    )
    view_online_button.pack(pady=20)


def show_label_menu():
    """Shows a list of context labels as buttons."""

    # Clear the main window.
    for widget in root.winfo_children():
        widget.destroy()

    # Create a button for each context label.
    for label_name in label_names:
        button = tk.Button(
            root,
            text=label_name,
            command=lambda o=label_name: label_selected_screen(o),
        )
        button.pack(fill=tk.BOTH, expand=True, pady=5)


# Create the main window
root = tk.Tk()
root.title("Simple Menu")
root.attributes("-topmost", True)

# Show the main menu initially
show_label_menu()

# Start the Tkinter event loop
root.mainloop()
