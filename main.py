from PyQt6.QtWidgets import QApplication

from main_window import MainWindow


def main():
    import pyaudio
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print(str(i).encode("cp1251").decode("utf-8"), str(p.get_device_info_by_index(i)['name']).encode("cp1251").decode("utf-8"))
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()


if __name__ == "__main__":
    main()

