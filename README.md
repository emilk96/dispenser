# Collector 

This folder can be used to start a virtual environment with the required python packages to run the GUI + motor control for the collector.

## How to run

1. Start venv
```
source bin/activate
```

2. Start GUI
```
python3 collector.py
```

## Important information 
- This setup was tested on a Raspberry Pi 4 running Raspberry Pi OS.
- Using keyboard listener to gather barcode scanner data sometimes results in a runtime error when the keyboard listener fails to stop, thus freezing the application. Maybe use second thread for keyboard listener that can be stopped from the outside. 
- The stepper motor python package in `collector/lib/python3.7/site-packages/rpi_python_drv8825/stepper.py` was modified to decrease step-size.
