#!/bin/bash
set -e

# ----------------------------------------
# Manu: setup Python 3.11 virtual environment (v1)
# ----------------------------------------

echo "Запуск setup окружения..."

# Директория, где лежит скрипт (это и есть v1)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "PROJECT_ROOT: $PROJECT_ROOT"

# Проверяем Python 3.11
if ! command -v python3.11 &> /dev/null; then
    echo "Python 3.11 не найден. Установите его перед запуском."
    exit 1
fi

PYTHON_VERSION=$(python3.11 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python найден: версия $PYTHON_VERSION"

VENV_PATH="$PROJECT_ROOT/.venv"

if [ -d "$VENV_PATH" ]; then
    echo "Виртуальное окружение уже существует."
else
    echo "Создаём виртуальное окружение..."
    python3.11 -m venv "$VENV_PATH"
fi

echo "Активируем виртуальное окружение..."
source "$VENV_PATH/bin/activate"

echo "Обновляем pip..."
python -m pip install --upgrade pip

if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    echo "Устанавливаем зависимости..."
    python -m pip install -r "$PROJECT_ROOT/requirements.txt"
else
    echo "Файл requirements.txt не найден!"
    exit 1
fi

echo ""
echo "✅ Готово. Виртуальное окружение настроено."
echo "Для ручной активации:"
echo "source $VENV_PATH/bin/activate"