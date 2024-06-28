import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QLineEdit, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt


class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle('To-Do List')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.task_list = QListWidget()
        self.layout.addWidget(self.task_list)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText('Title')
        self.layout.addWidget(self.title_input)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText('Description')
        self.layout.addWidget(self.description_input)

        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton('Add')
        self.add_button.clicked.connect(self.add_task)
        self.button_layout.addWidget(self.add_button)

        self.delete_button = QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete_task)
        self.button_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)
        self.load_tasks()

    def load_tasks(self):
        response = requests.get('http://127.0.0.1:8000/tasks/')
        if response.status_code == 200:
            tasks = response.json()
            self.task_list.clear()
            for task in tasks:
                if isinstance(task, dict):
                    self.task_list.addItem(
                        f"{task['id']}: {task['title']} - {task['description']}")

    def add_task(self):
        title = self.title_input.text()
        description = self.description_input.toPlainText()
        if title:
            response = requests.post(
                'http://127.0.0.1:8000/tasks/', data={'title': title, 'description': description})
            if response.status_code == 201:
                QMessageBox.information(
                    self, 'Success', 'Task added')
                self.load_tasks()
            else:
                QMessageBox.warning(self, 'Error', 'Could not add task')
        else:
            QMessageBox.warning(self, 'Error', 'Task title required')

    def delete_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            task_id = selected_item.text().split(':')[0]
            response = requests.delete(
                f'http://127.0.0.1:8000/tasks/{task_id}')
            if response.status_code == 204:
                QMessageBox.information(self, 'Success', 'Task deleted')
                self.load_tasks()
            else:
                QMessageBox.warning(self, 'Error', 'Could not delete task')
        else:
            QMessageBox.warning(self, 'Error', 'No task selected')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TodoApp()
    ex.show()
    sys.exit(app.exec())
