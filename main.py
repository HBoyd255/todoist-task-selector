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


for task in all_tasks:
    print(task)
    print()


