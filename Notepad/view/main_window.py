from PySide6.QtWidgets import *
from datetime import datetime
from Notepad.model.notepad import Notepad
from Notepad.controller.notepad_dao import DataBase


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setMinimumSize(700, 900)

        self.setWindowTitle('Bloco de Notas')

        self.lbl_id = QLabel('ID')
        self.txt_id = QLineEdit()
        self.lbl_note_name = QLabel('Titulo')
        self.txt_note_name = QLineEdit()
        self.lbl_note_date = QLabel('Data')
        self.txt_note_date = QLineEdit()
        # Criado nível de prioridade para o bloco de notas.
        self.lbl_priority = QLabel('Nivel de Prioridade')
        self.cb_priority = QComboBox()
        self.cb_priority.addItems(['Prioritário', 'Não prioritário'])
        self.lbl_note_text = QLabel('Texto')
        self.txt_note_text = QTextEdit()
        self.txt_id.setMaximumSize(40, 100)

        self.btn_save = QPushButton('Salvar')
        self.btn_save.setMaximumSize(150, 100)

        self.btn_remove = QPushButton('Remover')
        self.btn_remove.setMaximumSize(150, 100)

        self.note_table = QTableWidget()
        self.note_table.setColumnCount(5)
        self.note_table.setHorizontalHeaderLabels(['ID', 'Nome', 'Data', 'Nivel de prioridade', 'Texto'])

        self.note_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.note_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_note_name)
        layout.addWidget(self.txt_note_name)
        layout.addWidget(self.lbl_priority)
        layout.addWidget(self.cb_priority)
        layout.addWidget(self.lbl_note_text)
        layout.addWidget(self.txt_note_text)
        layout.addWidget(self.note_table)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_remove)

        self.btn_remove.setVisible(False)
        self.txt_id.setReadOnly(True)
        self.btn_save.clicked.connect(self.create_note)
        self.btn_remove.clicked.connect(self.delete_note)
        self.note_table.cellDoubleClicked.connect(self.load_note)
        self.fill_table()

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

    def create_note(self):
        db = DataBase()

        notepad = Notepad(
            note_name=self.txt_note_name.text(),
            note_date=datetime.today().date(),
            priority=self.cb_priority.currentText(),
            note_text=self.txt_note_text.toPlainText()
        )

        if self.btn_save.text() == 'Salvar':
            retorno = db.note_register(notepad)

            if retorno == 'Ok':
                msg = QMessageBox()
                msg.setWindowTitle('Bloco de notas')
                msg.setText('Bloco de notas criado')
                msg.exec()
                self.clear_field()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao criar')
                msg.setText(f'Erro ao criar bloco de notas')
                msg.exec()

        elif self.btn_save.text() == 'Atualizar':
            retorno = db.update_note(self.txt_id.text(), notepad)

            if retorno == 'Ok':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Notas atualizadas')
                msg.setText('Bloco de notas atualizada com sucesso')
                msg.exec()

                self.clear_field()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao atualizar')
                msg.setText('Erro ao atualizar bloco de notas')
                msg.exec()
        self.fill_table()
        self.txt_id.setReadOnly(True)

    def delete_note(self):
        msg = QMessageBox()
        msg.setWindowTitle('Bloco de notas removido')
        msg.setText(f'O bloco de notas fpo removido')
        msg.setInformativeText(f'Você deseja remover o bloco de notas {self.txt_note_name.text()} ?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText('Sim')
        msg.button(QMessageBox.No).setText('Não')
        answer = msg.exec()

        if answer == QMessageBox.Yes:
            db = DataBase()
            response = db.delete_note(self.txt_id.text())

            if response == 'Ok':
                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Nota deletado')
                nv_msg.setText('Bloco de notas deletado com sucesso')
                nv_msg.exec()
                self.clear_field()
            else:
                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Nota deletado')
                nv_msg.setText('Erro ao deletar bloco de notas')
                nv_msg.exec()
        self.fill_table()
        self.txt_id.setReadOnly(True)

    def clear_field(self):
        for widget in self.container.children():
            if isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)

        self.btn_remove.setVisible(False)
        self.btn_save.setText('Salvar')

        self.fill_table()
        self.txt_id.setReadOnly(True)

    def fill_table(self):
        self.note_table.setRowCount(0)
        db = DataBase()
        list_note = db.read_note()
        self.note_table.setRowCount(len(list_note))

        for line, note in enumerate(list_note):
            for column, values in enumerate(note):
                self.note_table.setItem(line, column, QTableWidgetItem(str(values)))

    def load_note(self, row):
        self.txt_id.setText(self.note_table.item(row, 0).text())
        self.txt_note_name.setText(self.note_table.item(row, 1).text())
        self.txt_note_date.setText(self.note_table.item(row, 2).text())
        priority_map = {'Prioritário': 0, 'Não prioritário': 1}
        self.cb_priority.setCurrentIndex(priority_map.get(self.note_table.item(row, 3).text(), 0))
        self.txt_note_text.setText(self.note_table.item(row, 4).text())
        self.btn_save.setText('Atualizar')
        self.btn_remove.setVisible(True)
        self.txt_id.setReadOnly(True)
