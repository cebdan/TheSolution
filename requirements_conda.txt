# Команды conda для установки зависимостей TheSolution
# Выполните эти команды в conda окружении

# Создание нового окружения (опционально)
# conda create -n thesolution python=3.9
# conda activate thesolution

# Основные зависимости через conda-forge
conda install -c conda-forge opencascade
conda install -c conda-forge qt
conda install -c conda-forge pyside6
conda install -c conda-forge numpy
conda install -c conda-forge scipy
conda install -c conda-forge matplotlib
conda install -c conda-forge pybind11
conda install -c conda-forge cmake
conda install -c conda-forge make

# Дополнительные Python пакеты через pip (если не найдены в conda)
pip install PyOpenGL
pip install PyOpenGL-accelerate
pip install PyYAML
pip install jsonschema
pip install pytest
pip install black
pip install flake8
pip install requests
pip install pillow

# Альтернативная установка всех зависимостей одной командой
# conda install -c conda-forge opencascade qt pyside6 numpy scipy matplotlib pybind11 cmake make
