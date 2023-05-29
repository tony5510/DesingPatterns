from abc import ABC, abstractmethod

# Абстрактный класс Task
class Task(ABC):
    @abstractmethod
    def create_task(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

# Конкретный класс PersonalTask
class PersonalTask(Task):
    def create_task(self):
        return PersonalTask()

    def get_description(self):
        return "Personal Task (Личная задача)"

# Конкретный класс WorkTask
class WorkTask(Task):
    def create_task(self):
        return WorkTask()

    def get_description(self):
        return "Work Task (Рабочая задача)"

# Конкретный класс ShoppingTask
class ShoppingTask(Task):
    def create_task(self):
        return ShoppingTask()

    def get_description(self):
        return "Shopping Task (Задача по совершению покупок)"

# Базовый класс декоратора
class TaskDecorator(Task):
    def __init__(self, task):
        self.task = task

    def create_task(self):
        return self.task.create_task()

    def get_description(self):
        return self.task.get_description()

# Конкретный класс PriorityTaskDecorator
class PriorityTaskDecorator(TaskDecorator):
    def create_task(self):
        return PriorityTaskDecorator(self.task.create_task())

    def get_description(self):
        return f"Priority Task (Задача с приоритетом): {self.task.get_description()}"

# Конкретный класс ReminderTaskDecorator
class ReminderTaskDecorator(TaskDecorator):
    def create_task(self):
        return ReminderTaskDecorator(self.task.create_task())

    def get_description(self):
        return f"Reminder Task (Задача с напоминанием): {self.task.get_description()}"

# Конкретный класс LabelTaskDecorator
class LabelTaskDecorator(TaskDecorator):
    def __init__(self, task, label):
        super().__init__(task)
        self.label = label

    def create_task(self):
        return LabelTaskDecorator(self.task.create_task(), self.label)

    def get_description(self):
        return f"Label Task (Задача с меткой): {self.task.get_description()} [{self.label}]"

# Абстрактный класс Команды
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

# Конкретный класс Команды - Создание задачи
class CreateTaskCommand(Command):
    def __init__(self, task_manager, task):
        self.task_manager = task_manager
        self.task = task

    def execute(self):
        self.task_manager.create_task(self.task)

# Конкретный класс Команды - Изменение статуса задачи
class ChangeStatusCommand(Command):
    def __init__(self, task_manager, task_id, status):
        self.task_manager = task_manager
        self.task_id = task_id
        self.status = status

    def execute(self):
        self.task_manager.change_task_status(self.task_id, self.status)

# Класс, который управляет задачами
class TaskManager:
    def create_task(self, task):
        print(f"Создание задачи: {task}")

    def change_task_status(self, task_id, status):
        print(f"Изменение статуса задачи {task_id} на {status}")

# Класс, представляющий клиентский код
class TaskApp:
    def __init__(self):
        self.task_manager = TaskManager()

    def create_task(self, task):
        command = CreateTaskCommand(self.task_manager, task)
        command.execute()

    def change_task_status(self, task_id, status):
        command = ChangeStatusCommand(self.task_manager, task_id, status)
        command.execute()

# Клиентский код
def main():
    # Создание задачи типа PersonalTask
    personal_task = PersonalTask().create_task()
    print(personal_task.get_description())

    # Декорирование задачи типа PersonalTask с приоритетом и напоминанием
    decorated_task = PriorityTaskDecorator(ReminderTaskDecorator(personal_task)).create_task()
    print(decorated_task.get_description())

    # Декорирование задачи типа WorkTask с меткой
    work_task = WorkTask().create_task()
    labeled_task = ReminderTaskDecorator(LabelTaskDecorator(work_task, "Важное")).create_task()
    print(labeled_task.get_description())

    # Создание приложения и использование команды для создания задачи
    app = TaskApp()
    app.create_task(decorated_task.get_description())

    # Использование команды для изменения статуса задачи
    app.change_task_status(1, "в процессе...")

if __name__ == '__main__':
    main()
