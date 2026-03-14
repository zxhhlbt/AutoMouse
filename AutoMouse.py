import sys
import threading
import time

import keyboard
from pynput.mouse import Controller
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


class MouseSimulator(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = False
        self.mouse = Controller()

    def run(self):
        pattern = [(0, -10), (0, 10), (-10, 0), (10, 0), (-10, 0), (10, 0)]

        while True:
            if self.running:
                for dx, dy in pattern:
                    if not self.running:
                        break

                    self.mouse.move(dx, dy)
                    time.sleep(0.2)

            else:
                time.sleep(0.1)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mouse Simulator")

        self.simulator = MouseSimulator()
        self.simulator.daemon = True
        self.simulator.start()

        layout = QVBoxLayout()

        self.hotkey_label = QLabel("ShortCut: unset")
        layout.addWidget(self.hotkey_label)

        self.btn_set = QPushButton("Setting ShortCut")
        layout.addWidget(self.btn_set)

        self.status = QLabel("Status: Stop")
        layout.addWidget(self.status)

        self.setLayout(layout)

        self.btn_set.clicked.connect(self.record_hotkey)

        self.current_hotkey = None

    def toggle(self):
        self.simulator.running = not self.simulator.running

        if self.simulator.running:
            self.status.setText("Status: Running")
        else:
            self.status.setText("Status: Stop")

    # 录制快捷键
    def record_hotkey(self):
        self.hotkey_label.setText("Please press the shortcut key...")

        threading.Thread(target=self._wait_hotkey, daemon=True).start()

    def _wait_hotkey(self):
        hotkey = keyboard.read_hotkey()

        if self.current_hotkey:
            keyboard.remove_hotkey(self.current_hotkey)

        self.current_hotkey = keyboard.add_hotkey(hotkey, self.toggle)

        self.hotkey_label.setText(f"ShortCut: {hotkey.upper()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(250, 150)
    window.show()

    sys.exit(app.exec())
