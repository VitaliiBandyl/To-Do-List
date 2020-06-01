from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

ENGINE = create_engine('sqlite:///todo.db?check_same_thread=False')
BASE = declarative_base()


class Task(BASE):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class ToDoList:
    def __init__(self, session):
        self.session = session

    def read_action(self):
        """Read user action from standard input"""

        actions = {
            1: self.show_today_tasks,
            2: self.show_weekly_tasks,
            3: self.show_all_tasks,
            4: self.add_task,
            0: self.exit
        }

        commands = [
            "1) Today's tasks",
            "2) Week's tasks",
            "3) All tasks",
            "4) Add task",
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

    def show_weekly_tasks(self):
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

    def exit(self):
        print("Bye!")
        self.session.close()


def main():
    BASE.metadata.create_all(ENGINE)
    Session = sessionmaker(bind=ENGINE)
    session = Session()
    my_to_do_list = ToDoList(session)
    my_to_do_list.read_action()


if __name__ == '__main__':
    main()
