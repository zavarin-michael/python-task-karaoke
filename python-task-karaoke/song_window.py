import copy
import datetime
import os
import time

import pygame
from PyQt6 import sip
from PyQt6.QtCore import QUrl, QThread, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget

import midi_parser
from recording import Recording, RecordingWindow


def get_label():
    label = QLabel()
    label.setMaximumHeight(50)
    label.setFont(QFont("Calibri", 15))
    label.setText(f'<font color="green"></font><font color="blue"></font>')
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    return label


class SongWindow(QMainWindow):
    def __init__(self, track, is_recording, parent=None):
        super(SongWindow, self).__init__(parent)

        self.window = QWidget()
        self.layout = QVBoxLayout()
        self.window.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.window.setStyleSheet('background-color: black;')

        self.videoWidget = QVideoWidget()

        self.lines = [get_label() for i in range(3)]

        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        print(QUrl.fromLocalFile(os.path.join("python-task-karaoke", "giga.mp4")))
        self.player.setSource(QUrl.fromLocalFile(os.path.join("python-task-karaoke", "giga.mp4")))
        self.audioOutput.setVolume(0)
        self.player.play()
        self.player.mediaStatusChanged.connect(self.status_changed)
        self.player.setVideoOutput(self.videoWidget)

        self.layout.addWidget(self.videoWidget)
        for i in self.lines:
            self.layout.addWidget(i)

        self.window.setLayout(self.layout)

        self.setWindowTitle(os.path.splitext(str(track))[0])
        self.setFixedSize(700, 700)
        self.setCentralWidget(self.window)

        self.text_tread = Timer(self.lines, track)
        self.text_tread.start()
        self.text_tread.finished.connect(self.close)

        self.is_recording = is_recording
        if is_recording:
            self.recording_tread = Recording()
            self.recording_tread.start()

    def status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.player.setPosition(0)
            self.player.play()

    def closeEvent(self, *args):
        super().closeEvent(*args)
        self.player.stop()
        sip.delete(self.player)
        self.text_tread.terminate()
        pygame.mixer.music.stop()
        self.parent().song_window = None

        if self.is_recording:
            self.recording_tread.recording = False
            time.sleep(0.2)
            self.parent().record_window = RecordingWindow(self.parent())
            self.parent().record_window.show()

        self.close()


class Timer(QThread):

    def __init__(self, lines, track):
        self.lines = lines
        self.track = track
        QThread.__init__(self)

    def __del__(self):
        pygame.mixer.music.stop()

    def run(self):
        time.sleep(1)

        m = midi_parser.MidiParser()
        m.load_file(self.track)

        pygame.mixer.init()
        pygame.mixer.music.load(self.track)
        pygame.mixer.music.play(0, 0)  # Start song at 0 and don't loop

        start = datetime.datetime.now()
        # start=start-datetime.timedelta(0,9) # To start lyrics at a later point
        dt = 0.0
        print(self.lines)

        preva = ["", "", ""]
        prevb = ["", "", ""]
        chet = 0

        while pygame.mixer.music.get_busy():
            dt = (datetime.datetime.now() - start).total_seconds()
            m.update_karaoke(dt)

            if m.karlinea[0] == "":
                for iline in range(3):
                    self.lines[iline].setText(
                        f'<font color="green">{preva[iline]}</font><font color="white">{prevb[iline]}</font>')
                chet += 1
            else:
                for iline in range(3):
                    self.lines[iline].setText(
                        f'<font color="green">{m.karlinea[iline]}</font><font color="white">{m.karlineb[iline]}</font>')
                chet = 0

            if chet == 0 or chet > 3:
                preva = copy.deepcopy(m.karlinea)
                prevb = copy.deepcopy(m.karlineb)

                if chet == 0:
                    for i in range(3):
                        preva[i] += prevb[i]
                        prevb[i] = ""
                chet = 0

            time.sleep(.1)

        time.sleep(1)
