# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем системные зависимости для OpenGL и Qt
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libegl1 \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxcb-xfixes0 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Копируем зависимости
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Копируем исходники
COPY src/ ./src/
COPY cpp_src/ ./cpp_src/

# Если C++ модуль уже собран — копируем
COPY build/motion_core.cpython-313-x86_64-linux-gnu.so src/motion_visualizer/cpp_bridge/ 2>/dev/null || true

# Настройка окружения
ENV PYTHONPATH=/app/src
ENV LD_LIBRARY_PATH=/app/src/motion_visualizer/cpp_bridge:$LD_LIBRARY_PATH
ENV QT_QPA_PLATFORM=xcb

# Запуск
CMD ["uv", "run", "python", "-m", "motion_visualizer.main"]