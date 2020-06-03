from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

ENGINE = create_engine('sqlite:///todo.db?check_same_thread=False')
BASE = declarative_base()


class Task(BASE):
    """Table in database"""

    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class TaskList:
    def __init__(self, session):
        self.session = session

    def read_action(self):
        """Read user action from standard input"""

        actions = {
            1: self.show_today_tasks,
            2: self.show_week_tasks,
            3: self.show_all_tasks,
            4: self.missed_tasks,
            5: self.add_task,
            6: self.delete_task,
            0: self.exit
        }

        commands = [
            "1) Today's tasks",
            "2) Week's tasks",
            "3) All tasks",
            "4) Missed tasks",
            "5) Add task",
            "6) Delete task",
            "0) Exit",
        ]
        print(*commands, sep="\n")

        action = int(input())
        print()
        actions[action]()

    def show_today_tasks(self):
        """Shows tasks due today"""

        today = datetime.today()
        tasks = self.session.query(Task).filter(Task.deadline == today.date()).all()
        print(f"Today {today.day} {today.strftime('%b')}:")
        if not tasks:
            print("Nothing to do!")
        else:
            for num, task in enumerate(tasks, start=1):
                print(f"{num}. {task}")

        self.read_action()

    def show_week_tasks(self):
        """Shows tasks due to week"""

        day = datetime.today()
        for _ in range(7):
            print(f"{day.strftime('%A %d %b')}:")

            tasks = self.session.query(Task).filter(Task.deadline == day.date()).all()
            if not tasks:
                print("Nothing to do!")
            for num, task in enumerate(tasks, start=1):
                print(f"{num}. {task}")
            print()

            day = day + timedelta(days=1)

        self.read_action()

    def show_all_tasks(self):
        """Shows all tasks"""

        tasks = self.session.query(Task).all()
        print("All tasks:")
        for num, task in enumerate(tasks, start=1):
            print(f"{num}. {task}. {task.deadline.day} {task.deadline.strftime('%b')}")

        self.read_action()

    def add_task(self):
        """Added new task to base"""

        print("Enter task")
        task = input()
        print("Enter deadline")
        deadline = input()
        format_ = "%Y-%m-%d"
        deadline = datetime.strptime(deadline, format_)

        new_task = Task(task=task, deadline=deadline)
        self.session.add(new_task)
        self.session.commit()

        print("The task has been added!")
        self.read_action()

    def missed_tasks(self):
        """Shows tasks whose deadline are missed"""
        today = datetime.today()

        tasks = self.session.query(Task).filter(Task.deadline < today.date()).all()
        print("Missed tasks:")
        for num, task in enumerate(tasks, start=1):
            print(f"{num}. {task}. {task.deadline.day} {task.deadline.strftime('%b')}")

        print()
        self.read_action()

    def delete_task(self):
        """Deletes tasks from database"""

        tasks = self.session.query(Task).all()
        print("Chose the number of the task you want to delete:")
        for num, task in enumerate(tasks, start=1):
            print(f"{num}. {task}. {task.deadline.day} {task.deadline.strftime('%b')}")

        n = int(input()) - 1  # Compensation enumerate start=1
        self.session.delete(tasks[n])
        self.session.commit()
        print("The task has been deleted!\n")
        self.read_action()

    def exit(self):
        print("Bye!")
        self.session.close()


def main():
    BASE.metadata.create_all(ENGINE)
    Session = sessionmaker(bind=ENGINE)
    session = Session()
    my_to_do_list = TaskList(session)
    my_to_do_list.read_action()


if __name__ == '__main__':
    main()
