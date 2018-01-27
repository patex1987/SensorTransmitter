from flask import Flask

from sensor_generator import Sensor

sensor = Sensor()
sensor.run_data_generation()

app = Flask(__name__)


from api_app import routes