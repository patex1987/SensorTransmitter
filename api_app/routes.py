from api_app import app
from api_app import sensor
from flask import request
from flask import abort
from flask import make_response
from flask import jsonify

@app.route('/sensor', methods=['GET'])
def get_timezones():
    '''handles timezone requests
    '''
    arguments = request.args
    if len(arguments) != 0:
        abort(400)
    actual_temp = sensor.actual_temperature
    result_val = {'temperature': actual_temp}
    return jsonify(result_val)


@app.errorhandler(400)
def not_found(error):
    '''error 400 handling
    '''
    error_msg = 'Error, wrong parameters'
    error_output = jsonify({'error': error_msg})
    return make_response(error_output, 400)