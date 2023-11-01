import wave

import pyaudio
from PyQt6 import QtCore, QtWidgets, sip
from PyQt6.QtCore import QThread, QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QMainWindow, QWidget

filename = "output_sound.wav"


class Recording(QThread):
    def __init__(self):
        self.recording = True
        QThread.__init__(self)

    def run(self):
        chunk = 1024  # Запись кусками по 1024 сэмпла
        sample_format = pyaudio.paInt16  # 16 бит на выборку
        channels = 1
        rate = 44100  # Запись со скоростью 44100 выборок(samples) в секунду
        p = pyaudio.PyAudio()  # Создать интерфейс для PortAudio

        print("Started recording...")

        stream = p.open(
            format=sample_format,
            channels=channels,
            rate=rate,
            frames_per_buffer=chunk,
            input=True,
        )

        frames = []  # Инициализировать массив для хранения кадров

        # Хранить данные в блоках в течение 3 секунд
        while self.recording:
            print("recording...")
            data = stream.read(chunk)
            frames.append(data)

        # Остановить и закрыть поток
        stream.stop_stream()
        stream.close()
        # Завершить интерфейс PortAudio
        p.terminate()

        print("Finished recording!")

        # Сохранить записанные данные в виде файла WAV
        wf = wave.open(filename, "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(rate)
        wf.writeframes(b"".join(frames))
        wf.close()


class RecordingWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dict = {
            "output_sound.wav": [],
        }
        self.song = ""
        self.widget = QWidget(self)
        self.player = QMediaPlayer(self)
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.audioOutput.setVolume(50)
        self.player.mediaStatusChanged.connect(self.playerState)

        self.qsl = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.qsl.sliderMoved.connect(self.SetPlayPosition)
        self.qsl.sliderReleased.connect(self.slider_released)

        self.box = QtWidgets.QVBoxLayout(self)

        self.setFixedSize(250, 120)
        self.setWindowTitle("Recording")

        for line, song in enumerate(self.dict):
            play_btn = QtWidgets.QPushButton("Play")
            print(song)
            play_btn.clicked.connect(lambda ch, song=song: self.play(song))

            pause_btn = QtWidgets.QPushButton("Pause")
            pause_btn.setEnabled(False)
            pause_btn.clicked.connect(self.pause)

            label = QtWidgets.QLabel(song)
            self.box.addWidget(play_btn, line)
            self.box.addWidget(pause_btn, line)
            self.box.addWidget(label, line)

            self.dict[song].append(play_btn)
            self.dict[song].append(pause_btn)

        self.box.addWidget(self.qsl)  # + , 1, 3

        self.widget.setLayout(self.box)
        self.setCentralWidget(self.widget)
        self.Play_Pause = True
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.PlayMode)
        self.timer.start(1000)

    def PlayMode(self):
        if not self.Play_Pause and self.player is not None:
            self.qsl.setMinimum(0)
            self.qsl.setMaximum(self.player.duration())
            self.qsl.setValue(self.qsl.value() + 1000)

    def slider_released(self):
        self.player.setPosition(self.qsl.value())
        if self.player.isAvailable():
            self.player.play()
            self.Play_Pause = False

    def SetPlayPosition(self, val):
        pass

    # Воспроизведение
    def play(self, song):
        if not self.player.isAvailable():
            self.player.setSource(QUrl.fromLocalFile(song))
            self.dict[song][1].setEnabled(True)
            self.song = song

        if self.song == song:
            pass
        else:
            self.player.setSource(QUrl.fromLocalFile(song))
            print(self.song)
            print(self.dict)
            if self.song != "":
                self.dict[self.song][1].setEnabled(False)
            self.dict[song][1].setEnabled(True)
            self.song = song

        self.player.play()
        self.Play_Pause = False

    def pause(self):
        self.player.pause()
        self.Play_Pause = True

    def playerState(self, state):
        if state == 0:
            self.Play_Pause = True
            self.qsl.setSliderPosition(0)

    def closeEvent(self, *args):
        self.player.stop()
        sip.delete(self.player)
        self.player = None
        self.close()
