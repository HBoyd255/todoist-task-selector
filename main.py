from todoist_api_python.api import TodoistAPI
from modules.file_utils import text_file_to_string, save_object, load_object

from modules.gui import GUI


# If set to True, the data will be loaded from the pickle files.
# If set to False, the data will be loaded from the Todoist API.
# This allows for faster testing.
LOAD_FROM_PICKLE = True

# The API key is stored in a text file to keep it secret from the git
# repository.
API_TEXT_FILE = "secrets/api_key.txt"
API_KEY = text_file_to_string(API_TEXT_FILE)

# Create an instance of the Todoist API.
api = TodoistAPI(API_KEY)


def get_data():

    if LOAD_FROM_PICKLE:
        all_tasks = load_object("secrets/tasks.pickle")
        all_labels = load_object("secrets/labels.pickle")
        all_projects = load_object("secrets/projects.pickle")

    else:
        all_tasks = api.get_tasks()
        all_labels = api.get_labels()
        all_projects = api.get_projects()

        save_object(all_tasks, "secrets/tasks.pickle")
        save_object(all_labels, "secrets/labels.pickle")
        save_object(all_projects, "secrets/projects.pickle")

    # Create a list of the label names.
    label_names = [label.name for label in all_labels]

    # Create a dictionary of project names.
    # This was the name of a project can be found by its ID.
    project_name_dict = {}

    for project in all_projects:
        project_name_dict[project.id] = project.name

    return label_names, all_tasks, project_name_dict


gui = GUI(get_data)

gui.run()
