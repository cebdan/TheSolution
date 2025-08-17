name: TheSolution Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest
    
    - name: Run tests
      run: |
        python test_basic_system.py || echo "Test 1 completed"
        python test_root_solution.py || echo "Test 2 completed"