import sys
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1117, 789)
        MainWindow.setWindowTitle("Работа с БД")

        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 20, 841, 711))

        font = QtGui.QFont()
        font.setPointSize(16)
        self.tableWidget.setFont(font)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(890, 150, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setText("Добавить")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(890, 300, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setText("Изменить")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(890, 450, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setText("Обновить")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(890, 610, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setText("Удалить")

        MainWindow.setCentralWidget(self.centralwidget)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.create_db()
        self.load_data()

        self.ui.pushButton.clicked.connect(self.add)
        self.ui.pushButton_2.clicked.connect(self.edit)
        self.ui.pushButton_3.clicked.connect(self.load_data)
        self.ui.pushButton_4.clicked.connect(self.delete)

    def create_db(self):

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            group_name TEXT
        )
        """)

        cursor.execute("SELECT COUNT(*) FROM students")

        conn.commit()
        conn.close()

    def load_data(self):

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()

        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Name", "Group"]
        )

        self.ui.tableWidget.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(value))

                if j == 0:
                    item.setFlags(QtCore.Qt.ItemIsEnabled)

                self.ui.tableWidget.setItem(i, j, item)

        conn.close()

    def add(self):

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students (name, group_name) VALUES ('Новый студент','000')"
        )

        conn.commit()
        conn.close()

        self.load_data()

    def edit(self):

        row = self.ui.tableWidget.currentRow()
        if row == -1:
            return

        record_id = self.ui.tableWidget.item(row, 0).text()
        name = self.ui.tableWidget.item(row, 1).text()
        group = self.ui.tableWidget.item(row, 2).text()

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE students SET name=?, group_name=? WHERE id=?",
            (name, group, record_id)
        )

        conn.commit()
        conn.close()

        self.load_data()

    def delete(self):

        row = self.ui.tableWidget.currentRow()
        if row == -1:
            return

        record_id = self.ui.tableWidget.item(row, 0).text()

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM students WHERE id=?",
            (record_id,)
        )

        conn.commit()
        conn.close()

        self.load_data()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
