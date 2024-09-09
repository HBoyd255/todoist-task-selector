import tkinter as tk
import random
import webbrowser
from typing import List
from todoist_api_python.models import Task

PAD_X = 10
PAD_Y = 5
CHOSEN_FONT = "Roboto Slab"


"""2-Bit colours
White      224,248,208
Light Gray 136,192,112
Dark Gray   52,104, 86
Black        8, 24, 32
"""

WHITE = "#e0f8d0"
LIGHT_GRAY = "#88c070"
DARK_GRAY = "#346856"
BLACK = "#081820"

# Define colors
BACKGROUND_COLOR = WHITE
TOP_MENU_COLOR = LIGHT_GRAY
BUTTON_COLOR = DARK_GRAY
TEXT_COLOR = BLACK
BUTTON_TEXT_COLOR = BLACK
PRESSED_BUTTON_COLOR = DARK_GRAY
PRESSED_BUTTON_TEXT_COLOR = BLACK


class GUI:
    def __init__(self, get_data_function) -> None:

        self._get_data_function = get_data_function

        self._root = tk.Tk()
        self._root.title("Todoist Task Selector")
        self._root.geometry("400x400")
        self._root.configure(bg=BACKGROUND_COLOR)

    def _filter_tasks_by_label(self, label_name: str) -> List[Task]:
        """Filters tasks by a label name."""

        return [task for task in self._all_tasks if label_name in task.labels]

    def _create_button(self, frame, text, command):
        """Creates a button with a given text and command."""

        button = tk.Button(
            frame,
            text=text,
            command=command,
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            activebackground=PRESSED_BUTTON_COLOR,
            activeforeground=PRESSED_BUTTON_TEXT_COLOR,
            font=(CHOSEN_FONT, 12),
        )

        return button

    def _show_context_menu(self):
        """Shows a list of context labels as buttons."""

        # Clear the main window.
        for widget in self._root.winfo_children():
            widget.destroy()

        button_frame = tk.Frame(self._root, bg=BACKGROUND_COLOR)
        button_frame.pack(fill=tk.BOTH, expand=True)

        # Create a button for each context label.
        for label_name in self._label_names:
            button = self._create_button(
                button_frame,
                label_name,
                lambda l=label_name: self._show_task_menu(l),
            )
            button.pack(fill=tk.BOTH, expand=True, padx=PAD_X, pady=PAD_Y)

    def _mark_task_as_done(self, task_to_remove, current_label):
        """Marks a task as done. This function does not remove the item from
        todoist, but instead removes it from the GUI. I don't want to use the
        api for anything other than getting data. To complete a task, press the
        "View Online Button" button, then the "Done" Button"""

        self._all_tasks = [
            task for task in self._all_tasks if task != task_to_remove
        ]

        self._show_task_menu(current_label)

    def _show_task_menu(self, label: str):
        """Display the menu that details a random task from a chosen context."""

        # Clear the main window.
        for widget in self._root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self._root, bg=BACKGROUND_COLOR)
        frame.pack(fill=tk.BOTH, expand=True)

        top_menu = tk.Frame(frame, bd=2, relief="solid", bg=TOP_MENU_COLOR)
        top_menu.pack(fill=tk.BOTH, expand=False)

        top_menu_left = tk.Frame(top_menu, bg=TOP_MENU_COLOR)
        top_menu_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        top_menu_right = tk.Frame(top_menu, bg=TOP_MENU_COLOR)
        top_menu_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        available_tasks = self._filter_tasks_by_label(label)

        task_count = len(available_tasks)

        back_button = self._create_button(
            top_menu_right, "Back", self._show_context_menu
        )

        # If there are no tasks, inform the user and add a return button.
        if task_count == 0:
            no_tasks_label = tk.Label(
                frame,
                text="There are no tasks in this context",
                font=(CHOSEN_FONT, 16),
                bg=BACKGROUND_COLOR,
                fg=TEXT_COLOR,
            )
            no_tasks_label.pack(pady=PAD_Y)
            back_button.pack(pady=PAD_Y)

            return

        random_task = random.choice(available_tasks)

        current_context_label = tk.Label(
            top_menu_left,
            text=f"Current Context: {label}",
            font=(CHOSEN_FONT, 10),
            bg=TOP_MENU_COLOR,
            fg=TEXT_COLOR,
        )
        current_context_label.pack(pady=PAD_Y, anchor="w")

        back_button.pack(pady=PAD_Y, anchor="e")

        task_count_label = tk.Label(
            top_menu_left,
            text=f"Available Tasks: {task_count}",
            font=(CHOSEN_FONT, 10),
            bg=TOP_MENU_COLOR,
            fg=TEXT_COLOR,
        )
        task_count_label.pack(pady=PAD_Y, anchor="w")

        done_button = self._create_button(
            top_menu_left,
            "Done",
            lambda: self._mark_task_as_done(random_task, label),
        )
        done_button.pack(pady=PAD_Y, anchor="w")

        reroll_button = self._create_button(
            top_menu_right, "Reroll", lambda: self._show_task_menu(label)
        )

        reroll_button.pack(pady=PAD_Y, anchor="e")

        # Selected Task Part
        selected_task_intro_label = tk.Label(
            frame,
            text="Selected Task:",
            font=(CHOSEN_FONT, 10),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
        )
        selected_task_intro_label.pack(pady=PAD_Y, anchor="w")

        task_name = random_task.content
        task_url = random_task.url
        task_description = random_task.description
        task_project_id = random_task.project_id

        task_name_label = tk.Label(
            frame,
            text=task_name,
            font=(CHOSEN_FONT, 16),
            wraplength=380,  # TODO update this to be dynamic
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
        )

        task_name_label.pack(pady=PAD_Y)

        task_description_label = tk.Label(
            frame,
            text=task_description,
            font=(CHOSEN_FONT, 10),
            wraplength=380,  # TODO update this to be dynamic
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
        )
        task_description_label.pack(pady=PAD_Y)

        bottom_menu = tk.Frame(frame, bg=BACKGROUND_COLOR)
        bottom_menu.pack(fill=tk.BOTH, expand=True, side="bottom", anchor="s")

        view_online_button = self._create_button(
            bottom_menu,
            "View Online",
            lambda url=task_url: webbrowser.open(url),
        )

        view_online_button.pack(pady=PAD_Y, side="right", anchor="se")

        project_name = self._project_name_dict[task_project_id]

        project_name_label = tk.Label(
            bottom_menu,
            text=f"Project: {project_name}",
            font=(CHOSEN_FONT, 10),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
        )

        project_name_label.pack(pady=PAD_Y, side="left", anchor="sw")

    def _start(self):
        """Initializes the GUI by getting the data and showing the context menu."""

        self._label_names, self._all_tasks, self._project_name_dict = (
            self._get_data_function()
        )

        self._show_context_menu()

    def _show_loading_screen(self):
        initial_frame = tk.Frame(self._root, bg=BACKGROUND_COLOR)
        initial_frame.pack(fill=tk.BOTH, expand=True)

        initial_label = tk.Label(
            initial_frame,
            text="Loading...",
            font=(CHOSEN_FONT, 16),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
        )
        initial_label.pack(pady=PAD_Y, expand=True)

    def run(self):

        self._show_loading_screen()

        self._root.after(100, self._start)

        # Start the Tkinter event loop
        self._root.mainloop()
