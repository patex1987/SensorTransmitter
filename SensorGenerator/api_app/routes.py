from api_app import app
from api_app import temperature_sensor, humidity_sensor
from flask import request
from flask import jsonify


class InvalidRequest(Exception):
    '''Exception class for handling invalid requests
    '''

    def __init__(self, message, status_code=400):
        '''InvalidRequest's __init__ method

        Args:
            message(str): error message
            status_code (int): HTTP status code, default value:400 (bad
                request)
        '''
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        '''Converts the object into a dictionary, useful for JSON
        serialization
        '''
        request_info = {}
        request_info['error'] = self.message
        return request_info


@app.route('/sensor', methods=['GET'])
def get_sensor_values():
    '''handles sensor requests
    '''
    arguments = request.args
    if arguments:
        raise InvalidRequest(message='No paramaters accepted')
    actual_temp = temperature_sensor.actual_value
    temp_unit = temperature_sensor.unit
    actual_humidity = humidity_sensor.actual_value
    humidity_unit = humidity_sensor.unit
    result_val = {
                    'temperature': {
                        'actual_value': actual_temp,
                        'unit': temp_unit
                    },
                    'humidity': {
                        'actual_value': actual_humidity,
                        'unit': humidity_unit
                    }
                 }
    return jsonify(result_val)


@app.errorhandler(InvalidRequest)
def handle_invalid_usage(error):
    '''Handling invalid requests
    '''
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
