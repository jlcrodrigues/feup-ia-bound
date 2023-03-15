# Bound

Bound game developed in Python.

## Steps to run

Assuming python is installed, run the main file:

```bash
pip install -r requirements.txt
cd src
python src/main.py
```

## Test

There is also a script included to run the game without the display, in order to test the bots more efficiently:

```bash
cd src
python src/main_dev.py
```

To run the tests, do:

```bash
cd src
python -m unittest discover -s test -p '*_test.py'
```
