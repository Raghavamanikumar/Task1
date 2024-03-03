import json
from datetime import datetime

class Task:
    def __init__(self, description, priority='medium', due_date=None, completed=False):
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = completed

    def __repr__(self):
        return f"Task('{self.description}', '{self.priority}', '{self.due_date}', {self.completed})"

class TaskManager:
    def __init__(self, file_path='tasks.json'):
        self.file_path = file_path
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.file_path, 'r') as file:
                tasks_data = json.load(file)
                print("Tasks Data:", tasks_data)  # Add this line to check tasks_data
                return [Task(**task_data) for task_data in tasks_data if task_data is not None]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open(self.file_path, 'w') as file:
            json.dump([task.__dict__ for task in self.tasks], file, default=self.json_serializable)

    def json_serializable(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return None

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, index):
        del self.tasks[index]
        self.save_tasks()

    def mark_completed(self, index):
        self.tasks[index].completed = True
        self.save_tasks()

    def list_tasks(self):
        for index, task in enumerate(self.tasks):
            print(f"{index+1}. {task.description} - Priority: {task.priority} - Due Date: {task.due_date} - Completed: {task.completed}")

# Example usage
if __name__ == "__main__":
    task_manager = TaskManager()

    while True:
        print("\n1. Add Task\n2. Remove Task\n3. Mark Task as Completed\n4. List Tasks\n5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            description = input("Enter task description: ")
            priority = input("Enter task priority (high/medium/low): ")
            due_date_str = input("Enter due date (YYYY-MM-DD): ")
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None
            task_manager.add_task(Task(description, priority, due_date))

        elif choice == '2':
            index = int(input("Enter task index to remove: ")) - 1
            task_manager.remove_task(index)

        elif choice == '3':
            index = int(input("Enter task index to mark as completed: ")) - 1
            task_manager.mark_completed(index)

        elif choice == '4':
            task_manager.list_tasks()

        elif choice == '5':
            break