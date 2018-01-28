# SensorTransmitter
> A simple threaded application generating random sensor data and transmitting them to a GUI

You can find a demo of the application on the following link: [video](https://streamable.com/cvf2k)

This repository contains 2 applications:

- `SensorGenerator`
	- A threaded application, simulates a behavior of a temperature and a humidity sensor. The data is transmitted using a Flask API
- `SensorProcessor`
	- GUI application developed using Qt. Downloads sensor data from the Flask API once per second and updates the GUI based on these values

## Installation

These modules were developed using the Anaconda distribution. The enviroment is exported to `sensor35.yml`. Python 3.5 is used

To create the same environment, use:
```
conda env create -f currency35.yml
```

If you are using a different distribution use `requirements.txt` (use with virtualenv)

More info to be added later

## Code

For more information about how the code works, check the docstrings in the code.

All the code has been revised with pylint


## Testing

Unit tests have been done for the `SensorGenerator` app
To run the tests use py.test

- `SensorGenerator\test_temperature_sensor.py`


Move to the `SensorGenerator` directory and try to run the following code:

```python
pytest test_temperature_sensor.py
```

## Usage example

- First run the Flask API
	+ go to the `SensorGenerator` directory
	+ run `python api_site.py`
	+ Normally the api resides on the following URL: `127.0.0.1:5000/sensor`
- Run the GUI application
	+ go to the `SensorProcessor` folder
	+ run `processor_gui.py`
	+ The GUI should show up
	+ Click on start to start receiving data


## Development setup

To be added later

## TODO

- Add unit tests for the GUI

## Release History


* 0.0.1
    * Work in progress

## Meta

Gabor Patassy – patex1987@gmail.com

[https://github.com/patex1987](https://github.com/patex1987)

## Contributing

To be added later
