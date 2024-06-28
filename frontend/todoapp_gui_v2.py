import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget,
    QTableWidgetItem, QFormLayout,
    QLineEdit, QWidget, QPushButton,
    QMessageBox, QTextEdit, QVBoxLayout
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction


class TodoApp(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('To-Do List')
        # self.setWindowIcon(QIcon('./assets/usergroup.png'))
        self.setGeometry(100, 100, 600, 400)

        self.tasks_list = self.get_tasks()

        self.todo_table = QTableWidget(self)
        self.setCentralWidget(self.todo_table)

        self.todo_table.setColumnCount(3)
        self.todo_table.setColumnWidth(0, 150)
        self.todo_table.setColumnWidth(1, 150)
        self.todo_table.setColumnWidth(2, 150)

        self.todo_table.setHorizontalHeaderLabels(
            ['Task', 'Description', 'Completed'])
        self.todo_table.setRowCount(len(self.tasks_list))

        # Create form
        form = QWidget()
        layout = QFormLayout(form)
        form.setLayout(layout)

        self.task_title = QLineEdit(form)
        self.task_description = QTextEdit(form)

        layout.addRow('Task', self.task_title)
        layout.addRow('Description', self.task_description)

        btn_add = QPushButton('Add')
        btn_add.clicked.connect(self.add_task)
        layout.addRow(btn_add)

        btn_delete = QPushButton('Delete')
        btn_delete.clicked.connect(self.delete_task)
        layout.addRow(btn_delete)

        # # Set layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.todo_table)
        main_layout.addWidget(form)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def get_tasks(self):
        try:
            response = requests.get('http://127.0.0.1:8000/tasks/')
            if response.status_code == 200:
                return response.json()
            else:
                QMessageBox.warning(self, 'Error', 'Could not fetch tasks')
                return []
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', str(e))
            return []

    def add_task(self):
        title = self.task_title.text()
        description = self.task_description.toPlainText()
        if title:
            response = requests.post(
                'http://127.0.0.1:8000/tasks/', data={'title': title, 'description': description})
            if response.status_code == 201:
                QMessageBox.information(
                    self, 'Success', 'Task added')
                self.update_tasks()
                self.clear_input()
            else:
                QMessageBox.warning(self, 'Error', 'Could not add task')
        else:
            QMessageBox.warning(self, 'Error', 'Task title required')

    def clear_input(self):
        self.task_title.clear()
        self.task_description.clear()

    def delete_task(self):
        selected_task = self.todo_table.currentRow()
        if selected_task >= 0:
            task_item = self.todo_table.item(selected_task, 0)
            if task_item:
                task_id = task_item.text()
                button = QMessageBox.question(
                    self,
                    'Confirmation',
                    'Are you sure that you want to delete the selected task?',
                    QMessageBox.StandardButton.Yes |
                    QMessageBox.StandardButton.No
                )
                if button == QMessageBox.StandardButton.Yes:
                    response = requests.delete(
                        f'http://127.0.0.1:8000/tasks/{task_id}')
                    if response == 204:
                        QMessageBox.information(
                            self, 'Success', 'Task deleted')
                    else:
                        QMessageBox.warning(
                            self, 'Warning', 'Could not delete task')
            else:
                QMessageBox.warning(self, 'Warning', 'No task selected')
        else:
            QMessageBox.warning(self, 'Warning', 'No task selected')

    def update_tasks(self):
        row = self.todo_table.rowCount()
        self.todo_table.insertRow(row)
        self.todo_table.setItem(row, 0, QTableWidgetItem(
            self.task_title.text()))
        self.todo_table.setItem(row, 1, QTableWidgetItem(
            self.task_description.toPlainText()))

        self.clear_input()
        self.make_tabels_read_only()

    def make_tabels_read_only(self):
        for row in range(self.todo_table.rowCount()):
            for column in range(self.todo_table.columnCount()):
                item = self.todo_table.item(row, column)
                if item:
                    item.setFlags(Qt.ItemFlag.ItemIsSelectable |
                                  Qt.ItemFlag.ItemIsEnabled)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TodoApp()
    ex.show()
    sys.exit(app.exec())
