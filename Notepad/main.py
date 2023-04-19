import sys

from PySide6.QtWidgets import QApplication

from controller.notepad_dao import DataBase
from view.main_window import MainWindow

db = DataBase()
db.connect()
db.create_table_notepad()
db.close_connection()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
