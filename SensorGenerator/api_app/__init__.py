from flask import Flask

from sensor_generator import Sensor

temperature_sensor = Sensor(min_value=10,
                            max_value=40,
                            unit='C',
                            move_range=(0.01, 1.0),
                            init_value=25)
temperature_sensor.run_data_generation()
humidity_sensor = Sensor(min_value=30,
                         max_value=80,
                         unit='%',
                         move_range=(0.01, 2.0),
                         init_value=60)
humidity_sensor.run_data_generation()

app = Flask(__name__)


from api_app import routes