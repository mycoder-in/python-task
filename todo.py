import os

FILE_NAME = 'todo.txt'

def load_tasks():
    """Load tasks from the file."""
    tasks = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as f:
            for line in f:
                tasks.append(line.strip().split(','))
    return tasks

def save_tasks(tasks):
    """Save tasks to the file."""
    with open(FILE_NAME, 'w') as f:
        for task, status in tasks:
            f.write(f"{task},{status}\n")

def view_tasks(tasks):
    """View all tasks."""
    if not tasks:
        print("No tasks in the list.")
        return

    print("\n--- To-Do List ---")
    for i, (task, status) in enumerate(tasks, 1):
        if status == 'complete':
            print(f"{i}. [✅] {task}")
        else:
            print(f"{i}. [ ] {task}")
    print("------------------\n")

def add_task(tasks):
    """Add a new task."""
    task = input("Enter the new task: ")
    if task:
        tasks.append([task, 'incomplete'])
        print(f'Task "{task}" added.')
    else:
        print("Task cannot be empty.")

def mark_task_complete(tasks):
    """Mark a task as complete."""
    view_tasks(tasks)
    try:
        task_num = int(input("Enter the number of the task to mark as complete: ")) - 1
        if 0 <= task_num < len(tasks):
            tasks[task_num][1] = 'complete'
            print(f'Task "{tasks[task_num][0]}" marked as complete.')
        else:
            print("Invalid task number.")
    except (ValueError, IndexError):
        print("Invalid input.")

def delete_task(tasks):
    """Delete a task."""
    view_tasks(tasks)
    try:
        task_num = int(input("Enter the number of the task to delete: ")) - 1
        if 0 <= task_num < len(tasks):
            removed_task = tasks.pop(task_num)
            print(f'Task "{removed_task[0]}" deleted.')
        else:
            print("Invalid task number.")
    except (ValueError, IndexError):
        print("Invalid input.")

def main():
    """Main function to run the to-do list application."""
    tasks = load_tasks()

    while True:
        print("\nWhat would you like to do?")
        print("1. View tasks")
        print("2. Add a new task")
        print("3. Mark a task as complete")
        print("4. Delete a task")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            mark_task_complete(tasks)
        elif choice == '4':
            delete_task(tasks)
        elif choice == '5':
            save_tasks(tasks)
            print("To-Do list saved. Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()