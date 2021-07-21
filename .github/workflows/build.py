name: PyWeather CI
on: [push]
jobs:
  build:

    timeout-minutes: 5
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.6, 3.7, 3.8]

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python3 -m pip install --upgrade pip
        python3 -m pip install .
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        python3 setup.py build_ext --inplace
    - name: Test with pytest
      run: |
        pytest
    # - name: Run tests
    #   run: |
    #     ./weather/stations/test/test_davis.py
    #     ./weather/stations/test/test_station.py