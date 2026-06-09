import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from motion_visualizer.visualization.glwidget import GLWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Motion Visualizer")
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.gl_widget = GLWidget()
        layout.addWidget(self.gl_widget)

        self.start_btn = QPushButton("Старт")
        self.start_btn.clicked.connect(self.on_start)
        layout.addWidget(self.start_btn)

    def on_start(self):
        print("[INFO] Кнопка Старт нажата. Завтра здесь будет движение.")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
