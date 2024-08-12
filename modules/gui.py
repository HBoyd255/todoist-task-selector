import tkinter as tk
import random
import webbrowser


class GUI:
    def __init__(self, label_names, all_tasks) -> None:
        self._label_names = label_names
        self._all_tasks = all_tasks

        self._root = tk.Tk()
        self._root.title("Todoist Task Selector")
        self._root.geometry("400x400")
        self._root.resizable(False, False)
        self._root.attributes("-topmost", True)

        self._show_context_menu()

    def _filter_tasks_by_label(self, label_name):
        """Filters tasks by a label name.

        Args:
            label_name (Str): The name of the label to filter by.

        Returns:
            (List): A list of tasks that have the specified label.
        """

        # Create an empty list of tasks to return.
        tasks_to_return = []

        # Iterate through each task.
        for task in self._all_tasks:
            # If the label name is in the task's labels, add the task to the list.
            if label_name in task.labels:
                tasks_to_return.append(task)

        # Return the list of tasks.
        return tasks_to_return

    def _show_context_menu(self):
        """Shows a list of context labels as buttons."""

        # Clear the main window.
        for widget in self._root.winfo_children():
            widget.destroy()

        # Create a button for each context label.
        for label_name in self._label_names:
            button = tk.Button(
                self._root,
                text=label_name,
                command=lambda l=label_name: self._show_task_menu(l),
            )
            button.pack(fill=tk.BOTH, expand=True, pady=5)

    def _show_task_menu(self, label):
        """Display the menu that details a random task from a chosen context."""

        # Clear the main window.
        for widget in self._root.winfo_children():
            widget.destroy()

        tasks_with_label = self._filter_tasks_by_label(label)

        task_count = len(tasks_with_label)

        task_count_label = tk.Label(
            self._root,
            text=f"There are {task_count} tasks",
            font=("Helvetica", 16),
        )
        task_count_label.pack(pady=20)

        back_button = tk.Button(
            self._root,
            text="Back",
            command=self._show_context_menu,
        )

        back_button.pack(pady=20)

        if task_count == 0:
            return

        reroll_button = tk.Button(
            self._root,
            text="Reroll",
            command=lambda o=label: self._show_task_menu(label),
        )
        reroll_button.pack(pady=20)

        random_task = random.choice(tasks_with_label)

        random_task_name = random_task.content
        random_task_url = random_task.url
        random_task_description = random_task.description

        task_name_label = tk.Label(
            self._root, text=f"Task: {random_task_name}", font=("Helvetica", 16)
        )

        task_name_label.pack(pady=20)

        if random_task_description:
            task_description_label = tk.Label(
                self._root,
                text=f"{random_task_description}",
                font=("Helvetica", 10),
            )
            task_description_label.pack(pady=20)

        view_online_button = tk.Button(
            self._root,
            text="View Online",
            command=lambda o=random_task_url: webbrowser.open(random_task_url),
        )
        view_online_button.pack(pady=20)

    def run(self):
        # Start the Tkinter event loop
        self._root.mainloop()
