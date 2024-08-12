# Todoist Task Selector

This is a simple Python program that uses the Todoist API to randomly select a
task, based on the current context(or label).

Based on the way I use Todoist, labels represent contexts. For example, any task
with the `@Home` label is a task that can be done at home. This program asks the
user for their current context, and then randomly selects a task from the list.

This is designed to be as simple as possible, similar to just pulling a task out
of a hat. It's not meant to be a full-featured task manager.


## Requirements

This script requires the `todoist-python` package version 2.1.3.