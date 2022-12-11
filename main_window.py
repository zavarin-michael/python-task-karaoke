import os

from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import QMainWindow, QPushButton, QFileDialog, QWidget, QLabel, QListWidget, QHBoxLayout, \
    QVBoxLayout, QLineEdit, QCheckBox

from search_logic import search
from song_window import SongWindow


class MenuAction(QAction):
    def __init__(self, *args, status_tip=None, func=None):
        super().__init__(*args)
        self.setStatusTip(status_tip)
        self.triggered.connect(func)


def get_name_tracks():
    tracks = os.listdir("tracks")
    tracks_str = []
    for file in tracks:
        tracks_str.append(os.path.splitext(str(file))[0])
    return tracks_str


def get_search_widget(func):
    search = QLineEdit()
    search.setPlaceholderText("Searching...")
    search.setFont(QFont("Calibri", 15))
    search.textChanged.connect(func)
    return search


def get_list_widget(l: list):
    list = QListWidget()
    for file in l:
        list.addItem(os.path.splitext(str(file))[0])
    list.setFont(QFont("Calibri", 15))
    return list


def get_checkbox():
    checkbox = QCheckBox("Recording your voice?")
    checkbox.setFont(QFont("Calibri", 15))
    checkbox.setChecked(True)
    return checkbox


def get_button(on_button_clicked):
    button = QPushButton("Play!")
    button.clicked.connect(on_button_clicked)
    button.setFont(QFont("Calibri", 15))
    return button


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.window = QWidget()

        self.search = get_search_widget(self.on_text_changed)
        self.tracks = get_name_tracks()
        self.checkbox = get_checkbox()
        self.list = get_list_widget(self.tracks)
        self.button = get_button(self.on_button_clicked)

        self.layout.addWidget(self.search)
        self.layout.addWidget(self.list)
        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.button)

        self.window.setLayout(self.layout)

        self.setCentralWidget(self.window)
        self.window.show()

        self.setFixedSize(400, 600)
        self.setWindowTitle('Python Karaoke')

        self.show()

    def on_text_changed(self, text):
        new_list = search(text, self.tracks)

        self.list.clear()
        for file in new_list:
            self.list.addItem(file)
        self.list.update()

    def on_button_clicked(self, action):
        if self.list.currentItem() is not None:
            self.song_window = SongWindow(f"tracks\{str(self.list.currentItem().text())}.kar",
                                          self.checkbox.isChecked(), self)
            self.song_window.show()

    def open_window(self, s, window):
        if len(list(filter(lambda x: type(x) == window, self.windows))) == 0:
            t = window(self)
            self.windows.append(t)
            t.show()
