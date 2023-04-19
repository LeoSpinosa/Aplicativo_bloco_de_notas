import sqlite3

from Notepad.model.notepad import Notepad


class DataBase:

    def __init__(self, nome='system.db'):
        self.connection = None
        self.name = nome

    def connect(self):
        self.connection = sqlite3.connect(self.name)

    def close_connection(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            print(e)

    def create_table_notepad(self):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS NOTEPAD(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOTE_NAME TEXT,
            NOTE_DATE DATE,
            PRIORITY TEXT,
            NOTE_TEXT TEXT
            );

            """
        )
        self.close_connection()

    def note_register(self, notepad=Notepad):
        self.connect()
        cursor = self.connection.cursor()
        note_field = ('NOTE_NAME', 'NOTE_DATE', 'PRIORITY', 'NOTE_TEXT')

        values = f"'{notepad.note_name}', '{notepad.note_date}', '{notepad.priority}', '{notepad.note_text}'"

        try:
            cursor.execute(f""" INSERT INTO NOTEPAD {note_field} VALUES ({values}) """)
            self.connection.commit()
            return 'Ok'
        except sqlite3.Error as e:
            return e
        finally:
            self.close_connection()

    def read_note(self):
        self.connect()

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM NOTEPAD")
            notes = cursor.fetchall()
            return notes
        except sqlite3.Error as e:
            print(f'Erro {e}')
            return None
        finally:
            self.close_connection()

    def update_note(self, id, note=Notepad):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(f""" UPDATE NOTEPAD SET 
                NOTE_NAME = '{note.note_name}', 
                NOTE_DATE = '{note.note_date}', 
                PRIORITY = '{note.priority}',
                NOTE_TEXT = '{note.note_text}' 
                WHERE ID  = '{id}'""")
            self.connection.commit()
            return 'Ok'
        except sqlite3.Error as e:
            print(e)
        finally:
            self.close_connection()

    def delete_note(self, id):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(f""" DELETE FROM NOTEPAD WHERE ID = '{id}' """)
            self.connection.commit()
            return 'Ok'
        except sqlite3.Error as e:
            print(e)
        finally:
            self.close_connection()
