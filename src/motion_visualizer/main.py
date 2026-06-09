# Импорт C++ модуля
# Импорт C++ модуля
import os

# Импорт C++ модуля
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

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "cpp_bridge"))
try:
    import motion_core

    print("✅ C++ module loaded")
except ImportError as e:
    print(f"❌ C++ module not loaded: {e}")
    motion_core = None


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

        # Таймер для обнавления анимации
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)

        if motion_core:
            self.integrator = motion_core.Integrator()
            self.integrator.set_speed(50.0, 50.0)  # Скорость пикселей в секунду
        else:
            self.integrator = None

    def on_start(self):
        print("[INFO] Кнопка Старт нажата. Завтра здесь будет движение.")

    def on_start(self):
        if self.integrator:
            self.integrator.reset()
            self.timer.start(16)  # ~60 FPS

    def update_simulation(self):
        if self.integrator:
            self.integrator.update(0.016)  # Шаг 16 мс
            x = self.integrator.get_x()
            y = self.integrator.get_y()
            self.gl_widget.set_position(x, y)
            if x > 800 or y > 600:
                self.timer.stop()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
