import tkinter as tk
import random
import webbrowser
from typing import List
from todoist_api_python.models import Task

PAD_Y = 5


class GUI:
    def __init__(
        self,
        label_names: List[str],
        all_tasks: List[Task],
        project_name_dict: dict,
    ) -> None:
        self._label_names = label_names
        self._all_tasks = all_tasks
        self._project_name_dict = project_name_dict

        self._root = tk.Tk()
        self._root.title("Todoist Task Selector")
        self._root.geometry("400x400")

        self._root.attributes("-topmost", True)

        self._show_task_menu("Home")

    def _filter_tasks_by_label(self, label_name: str) -> List[Task]:
        """Filters tasks by a label name."""

        return [task for task in self._all_tasks if label_name in task.labels]

    def _show_context_menu(self):
        """Shows a list of context labels as buttons."""

        # Clear the main window.
        for widget in self._root.winfo_children():
            widget.destroy()

        button_frame = tk.Frame(self._root)
        button_frame.pack(fill=tk.BOTH, expand=True)

        # Create a button for each context label.
        for label_name in self._label_names:
            button = tk.Button(
                button_frame,
                text=label_name,
                command=lambda l=label_name: self._show_task_menu(l),
            )
            button.pack(fill=tk.BOTH, expand=True)

    def _show_task_menu(self, label: str):
        """Display the menu that details a random task from a chosen context."""

        # Clear the main window.
        for widget in self._root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self._root)
        frame.pack(fill=tk.BOTH, expand=True)

        top_menu = tk.Frame(frame, bd=2, relief="solid")
        top_menu.pack(fill=tk.BOTH, expand=False)

        top_menu_left = tk.Frame(top_menu)
        top_menu_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        top_menu_right = tk.Frame(top_menu)
        top_menu_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        available_tasks = self._filter_tasks_by_label(label)

        task_count = len(available_tasks)

        back_button = tk.Button(
            top_menu_right,
            text="Back",
            command=self._show_context_menu,
        )

        # If there are no tasks, inform the user and add a return button.
        if task_count == 0:
            no_tasks_label = tk.Label(
                frame,
                text="There are no tasks in this context",
                font=("Helvetica", 16),
            )
            no_tasks_label.pack(pady=PAD_Y)
            back_button.pack(pady=PAD_Y)

            return

        current_context_label = tk.Label(
            top_menu_left,
            text=f"Current Context: {label}",
            font=("Helvetica", 10),
        )
        current_context_label.pack(
            pady=PAD_Y,
            anchor="w",
        )

        back_button.pack(
            pady=PAD_Y,
            anchor="e",
        )

        task_count_label = tk.Label(
            top_menu_left,
            text=f"Available Tasks: {task_count}",
            font=("Helvetica", 10),
        )
        task_count_label.pack(
            pady=PAD_Y,
            anchor="w",
        )

        reroll_button = tk.Button(
            top_menu_right,
            text="Reroll",
            command=lambda o=label: self._show_task_menu(label),
        )
        reroll_button.pack(
            pady=PAD_Y,
            anchor="e",
        )

        # Selected Task Part
        selected_task_intro_label = tk.Label(
            frame,
            text="Selected Task:",
            font=("Helvetica", 10),
        )
        selected_task_intro_label.pack(pady=PAD_Y, anchor="w")

        random_task = random.choice(available_tasks)

        task_name = random_task.content
        task_url = random_task.url
        task_description = random_task.description
        task_project_id = random_task.project_id

        task_name_label = tk.Label(
            frame,
            text=task_name,
            font=("Helvetica", 16),
            wraplength=380,  # TODO update this to be dynamic
        )

        task_name_label.pack(pady=PAD_Y)

        task_description_label = tk.Label(
            frame,
            text=task_description,
            font=("Helvetica", 10),
        )
        task_description_label.pack(pady=PAD_Y)

        bottom_menu = tk.Frame(frame)
        bottom_menu.pack(fill=tk.BOTH, expand=True, side="bottom", anchor="s")

        view_online_button = tk.Button(
            bottom_menu,
            text="View Online",
            command=lambda o=task_url: webbrowser.open(task_url),
        )

        view_online_button.pack(pady=PAD_Y, side="right", anchor="se")

        project_name = self._project_name_dict[task_project_id]

        project_name_label = tk.Label(
            bottom_menu,
            text=f"Project: {project_name}",
            font=("Helvetica", 10),
        )

        project_name_label.pack(pady=PAD_Y, side="left", anchor="sw")

        print(random_task)

    def run(self):
        # Start the Tkinter event loop
        self._root.mainloop()
