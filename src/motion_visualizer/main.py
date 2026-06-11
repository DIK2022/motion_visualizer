import os
import sys
import time

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QTextEdit,
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

from src.motion_visualizer.database.db_client import DatabaseClient


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

        self.reset_btn = QPushButton("Сброс")
        self.reset_btn.clicked.connect(self.on_reset)

        self.show_log_btn = QPushButton("Показать логи")
        self.show_log_btn.clicked.connect(self.show_logs)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addWidget(self.show_log_btn)
        layout.addLayout(btn_layout)

        # Лог-виджет для истории
        self.log_widget = QTextEdit()
        self.log_widget.setMaximumHeight(150)
        self.log_widget.setReadOnly(True)
        layout.addWidget(self.log_widget)

        # Таймер для обнавления анимации
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)

        # C++ интегратор
        if motion_core:
            self.integrator = motion_core.Integrator()
            self.integrator.set_speed(50.0, 50.0)  # Скорость пикселей в секунду
        else:
            self.integrator = None

        # База данных
        self.db = DatabaseClient("motion_logs.db")
        self.current_trial_id = None
        self.start_time = None
        self.finished = False

    def on_start(self):
        if self.integrator and not self.timer.isActive():
            self.integrator.reset()
            self.start_time = time.time()
            # Создаем запись в БД
            self.current_trial_id = self.db.create_trial("TestRun")
            self.log_message(f"Старт испытания ID={self.current_trial_id}")
            self.timer.start(16) # ~60 FPS
            self.finished = False


    def update_simulation(self):
        if self.integrator:
            self.integrator.update(0.016)  # Шаг 16 мс
            x = self.integrator.get_x()
            y = self.integrator.get_y()
            self.gl_widget.set_position(x, y)
            
            # Проверка финиша (услованая граница)
            if x > 800 or y > 600:
                self.timer.stop()
                if not self.finished:
                    duration = time.time() - self.start_time
                    distance = ((x**2 + y**2)**0.5) # пример: евклидово растояние
                    self.db.finish_trial(self.current_trial_id, duration, distance)
                    self.log_message(f"Финиш! Время: {duration:.2f}с, Дистанция: {distance:.1f}px")
                    self.finished = True
    
    def on_reset(self):
        if self.timer.isActive():
            self.timer.stop()
        if self.integrator:
            self.integrator.reset()
            self.gl_widget.set_position(0, 0)
            if self.current_trial_id and not self.finished:
                self.db.reset_trial(self.current_trial_id)
                self.log_message(f"Испытание ID={self.current_trial_id} сброшено пользователем")
            self.current_trial_id = None
            self.finished = False

    def show_logs(self):
        trials = self.db.get_all_trials()
        if not trials:
            self.log_message("Нет записи в базе данных.")
            return
        log_text = "\n=== История исполнений ===\n"
        for t in trials:
            log_text += f"ID:{t.id} | {t.scenario_name} | {t.start_time.strftime('%H:%M:%S')} |\
                            {t.status} | duration:{t.duration:.2f}с | dist:{t.distance:.1f}\n"
        self.log_widget.setText(log_text)

    def log_message(self, msg):
        current = self.log_widget.toPlainText()
        self.log_widget.setText(f"{current}\n[{time.strftime('%H:%M:%S')}] {msg}")



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
