from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker

ENGINE = create_engine('sqlite:///todo.db?check_same_thread=False')
BASE = declarative_base()


class Task(BASE):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"{self.id}. {self.task}"


class ToDoList:
    def __init__(self, session):
        self.session = session

    def read_action(self):
        """Read user action from standard input"""

        actions = {
            1: self.today_tasks,
            2: self.add_task,
            0: self.exit
        }

        commands = [
            "1) Today's tasks",
            "2) Add task",
            "0) Exit"
        ]
        print(*commands, sep="\n")

        action = int(input())
        print()
        actions[action]()

    def today_tasks(self):
        """Prints tasks due today"""

        tasks = self.session.query(Task).all()
        print("Today:")
        if not tasks:
            print("Nothing to do!")
        else:
            for task in tasks:
                print(task)

        self.read_action()

    def add_task(self):
        """Added new task to base"""

        print("Enter task")
        task = input()

        new_task = Task(task=task)
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
