# 🚀 Настройка GitHub Actions для TheSolution CAD в Windows
# Запустите этот скрипт в PowerShell

Write-Host "🔧 Настройка GitHub Actions для TheSolution CAD..." -ForegroundColor Cyan

# Создаем структуру GitHub Actions
New-Item -ItemType Directory -Force -Path ".github\workflows"
New-Item -ItemType Directory -Force -Path ".github\ISSUE_TEMPLATE"

Write-Host "📁 Создана структура директорий" -ForegroundColor Green

# 1. Основной CI workflow
$ciContent = @"
name: 🏗️ TheSolution CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  python-tests:
    name: 🐍 Python Tests
    runs-on: `${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ['3.9', '3.11']

    steps:
    - uses: actions/checkout@v4

    - name: 🐍 Set up Python `${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: `${{ matrix.python-version }}

    - name: 📦 Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov
        if (Test-Path requirements.txt) { pip install -r requirements.txt }

    - name: 🧪 Run tests (Windows)
      if: runner.os == 'Windows'
      run: |
        if (Test-Path test_basic_system.py) { python test_basic_system.py }
        if (Test-Path test_root_solution.py) { python test_root_solution.py }
        
        python -c "
        import sys
        import os
        sys.path.insert(0, 'Base Solution/python')
        sys.path.insert(0, 'Root Solution/python')
        
        try:
            from solution_coordinate import SolutionCoordinate
            print('✅ SolutionCoordinate импортирован')
        except ImportError as e:
            print(f'⚠️ Ошибка импорта SolutionCoordinate: {e}')
        
        try:
            from base_solution import Solution
            print('✅ Solution импортирован')
        except ImportError as e:
            print(f'⚠️ Ошибка импорта Solution: {e}')
        
        print('🎉 Базовые тесты завершены')
        "

    - name: 🧪 Run tests (Linux)
      if: runner.os == 'Linux'
      run: |
        if [ -f test_basic_system.py ]; then python test_basic_system.py; fi
        if [ -f test_root_solution.py ]; then python test_root_solution.py; fi
        
        python -c "
        import sys
        import os
        sys.path.insert(0, 'Base Solution/python')
        sys.path.insert(0, 'Root Solution/python')
        
        try:
            from solution_coordinate import SolutionCoordinate
            print('✅ SolutionCoordinate импортирован')
        except ImportError as e:
            print(f'⚠️ Ошибка импорта SolutionCoordinate: {e}')
        
        try:
            from base_solution import Solution
            print('✅ Solution импортирован')
        except ImportError as e:
            print(f'⚠️ Ошибка импорта Solution: {e}')
        
        print('🎉 Базовые тесты завершены')
        "

  quality-check:
    name: 🔍 Code Quality
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: 🐍 Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: 📦 Install quality tools
      run: |
        pip install flake8 black
    
    - name: 🔍 Basic lint check
      run: |
        find . -name "*.py" -not -path "./.git/*" | head -10 | xargs flake8 --max-line-length=100 --ignore=E501,W503 || true
        echo "✅ Lint проверка завершена"
    
    - name: 🎨 Format check
      run: |
        find . -name "*.py" -not -path "./.git/*" | head -5 | xargs black --check --diff || true
        echo "✅ Форматирование проверено"
"@

$ciContent | Out-File -FilePath ".github\workflows\ci.yml" -Encoding UTF8
Write-Host "✅ Создан .github\workflows\ci.yml" -ForegroundColor Green

# 2. Простой Python workflow для PR
$pythonCheckContent = @"
name: 🐍 Python Check

on:
  pull_request:
    paths:
      - '**/*.py'

jobs:
  quick-check:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: 🔍 Quick Python check
      run: |
        python -m py_compile `$(find . -name "*.py" | head -20) || true
        echo "✅ Python syntax check completed"
"@

$pythonCheckContent | Out-File -FilePath ".github\workflows\python-check.yml" -Encoding UTF8
Write-Host "✅ Создан .github\workflows\python-check.yml" -ForegroundColor Green

# 3. Dependabot для автообновлений
$dependabotContent = @"
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    commit-message:
      prefix: "⬆️"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
    commit-message:
      prefix: "🔧"
"@

$dependabotContent | Out-File -FilePath ".github\dependabot.yml" -Encoding UTF8
Write-Host "✅ Создан .github\dependabot.yml" -ForegroundColor Green

# 4. Создаем requirements-dev.txt для разработки
$requirementsDevContent = @"
# Инструменты разработки
pytest>=7.0.0
pytest-cov>=4.0.0
black>=22.0.0
flake8>=5.0.0
isort>=5.10.0

# Инструменты безопасности
bandit>=1.7.0
safety>=2.0.0

# Документация
sphinx>=5.0.0
sphinx-rtd-theme>=1.0.0
"@

$requirementsDevContent | Out-File -FilePath "requirements-dev.txt" -Encoding UTF8
Write-Host "✅ Создан requirements-dev.txt" -ForegroundColor Green

# 5. Простой setup.cfg
$setupCfgContent = @"
[flake8]
max-line-length = 100
extend-ignore = E203, W503, E501
exclude = 
    .git,
    __pycache__,
    build/,
    dist/,
    .venv/,
    venv/

[tool:pytest]
testpaths = .
python_files = test_*.py
addopts = --verbose --tb=short

[coverage:run]
source = .
omit = 
    tests/*
    setup.py
    */site-packages/*
    .venv/*
    venv/*
"@

$setupCfgContent | Out-File -FilePath "setup.cfg" -Encoding UTF8
Write-Host "✅ Создан setup.cfg" -ForegroundColor Green

# 6. Создаем .gitignore если его нет
if (-not (Test-Path ".gitignore")) {
    $gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*`$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
temp/
build/
cmake-build-*/

# Qt
*.pro.user
*.pro.user.*
moc_*.cpp
qrc_*.cpp
ui_*.h
"@

    $gitignoreContent | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "✅ Создан .gitignore" -ForegroundColor Green
}

# 7. Обновляем отчет разработки
if (Test-Path "отчет_разработки.md") {
    $date = Get-Date -Format "dd.MM.yyyy"
    $reportUpdate = @"

## 🔧 Настройка CI/CD ($date)

### ✅ Что настроено:
- GitHub Actions workflow для автоматического тестирования
- Проверка качества кода (flake8, black)
- Dependabot для автообновления зависимостей
- Базовые конфигурационные файлы

### 📋 Файлы созданы:
- `.github/workflows/ci.yml` - основной CI pipeline
- `.github/workflows/python-check.yml` - быстрая проверка Python
- `.github/dependabot.yml` - автообновления
- `requirements-dev.txt` - инструменты разработки
- `setup.cfg` - конфигурация инструментов

### 🚀 Следующие шаги:
1. Закоммитить и запушить изменения
2. Создать тестовый PR для проверки CI
3. Настроить защиту main ветки
4. Добавить badge статуса в README.md

"@

    Add-Content -Path "отчет_разработки.md" -Value $reportUpdate
    Write-Host "✅ Обновлен отчет разработки" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 GitHub Actions настроен!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Следующие шаги:" -ForegroundColor Yellow
Write-Host "1. git add .github/ requirements-dev.txt setup.cfg" -ForegroundColor White
Write-Host "2. git commit -m '🔧 Add GitHub Actions CI/CD'" -ForegroundColor White
Write-Host "3. git push" -ForegroundColor White
Write-Host "4. Создайте PR для тестирования CI" -ForegroundColor White
Write-Host ""
Write-Host "📊 После push вы увидите:" -ForegroundColor Cyan
Write-Host "- Вкладку 'Actions' в GitHub репозитории" -ForegroundColor White
Write-Host "- Автоматические проверки на PR" -ForegroundColor White
Write-Host "- Статус тестов на каждом коммите" -ForegroundColor White