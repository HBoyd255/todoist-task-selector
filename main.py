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


if LOAD_FROM_PICKLE:
    all_tasks = load_object("secrets/tasks.pickle")
    labels = load_object("secrets/labels.pickle")

else:
    all_tasks = api.get_tasks()
    labels = api.get_labels()

    save_object(all_tasks, "secrets/tasks.pickle")
    save_object(labels, "secrets/labels.pickle")




label_names = [label.name for label in labels]

gui = GUI(label_names,all_tasks)

gui.run()
