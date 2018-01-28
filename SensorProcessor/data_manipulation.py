from PyQt4.QtCore import QThread, SIGNAL, QTimer
from ring_buffer import RingBuffer
import requests
from requests.exceptions import ConnectionError
import numpy as np
from collections import namedtuple


class NoDataError(Exception):
    pass


class GetSensorsThread(QThread):
    def __init__(self, start_thread=False, update_interval_secs=1):
        '''
        method constructor
        '''
        super().__init__()
        self.start_thread = start_thread
        self.update_interval_secs = update_interval_secs

    def __del__(self):
        self.wait()

    def _get_sensor_data(self):
        '''Downloads the data from the API
        '''
        try:
            response = requests.get('http://127.0.0.1:5000/sensor')
        except ConnectionError:
            raise NoDataError
        if response.status_code != 200:
            raise NoDataError
        actual_values = response.json()
        if not 'temperature' in actual_values.keys() or \
           not 'humidity' in actual_values.keys():
            raise NoDataError
        return actual_values

    def run(self):
        '''Runs the thread until a signal is sent by the main thread to stop
        '''
        while self.start_thread:
            try:
                actual_values = self._get_sensor_data()
                self.emit(SIGNAL('update_values(PyQt_PyObject)'),
                          actual_values)
                print('IN THREAD')
                self.sleep(self.update_interval_secs)
                #self.msleep(15)
            except NoDataError:
                self.emit(SIGNAL('handle_error()'))


class ProcessActuators(QThread):
    '''This thread processes the actual values of the sensors and compares
    them to the limit values
    
    I.e. calculates the states of the actuators
    '''
    def __init__(self,
                 actual_temperature,
                 actual_humidity,
                 lower_temp_limit,
                 upper_temp_limit,
                 humidity_limit=40,
                 min_voltage=0,
                 max_voltage=10000):
        '''
        method constructor
        '''
        super().__init__()
        self._actual_temperature = actual_temperature
        self._actual_humidity = actual_humidity
        self._lower_temp_limit = lower_temp_limit
        self._upper_temp_limit = upper_temp_limit
        self._humidity_limit = humidity_limit
        self._min_voltage = min_voltage
        self._max_voltage = max_voltage
 

    def __del__(self):
        self.wait()

    def run(self):
        '''Calculates the output states of the actuators
        '''
        Actuators = collections.namedtuple('Actuators',
                                           'heating cooling ventilation')
        heating = int(self._actual_temperature < self._lower_temp_limit)
        cooling = int(self._actual_temperature > self._upper_temp_limit)
        ventilation = self._calculate_ventilation_state()
        actual_actuators = Actuators(heating=heating,
                                     cooling=cooling,
                                     ventilation=ventilation)
        self.emit(SIGNAL('actuator_values(PyQt_PyObject)'),
                  actual_actuators)

    def _calculate_ventilation_state(self)
        '''based on linear regression calculates the voltage of the
        ventilation
        '''
        coeff_a = self._max_voltage - self._min_voltage
        coeff_b = self.min_voltage - (coeff_a*self._humidity_limit)
        output_voltage = (coeff_a*self._actual_humidity) + coeff_b
        


class XYBuffer(object):
    '''A class for holding X and Y about the sensor

    Normally we would like to hold data for the last hour
    This class can be used for plotting sensor data as a moving window
    '''
    def __init__(self, update_interval_secs, total_secs=3600,
                 data_type=float):
        '''XYBuffer constructor
        '''
        self.buffer_size = total_secs // update_interval_secs
        self.x_buffer = RingBuffer(size_max=self.buffer_size,
                                   default_value=0,
                                   dtype=np.uint32)
        self.y_buffer = RingBuffer(size_max=self.buffer_size,
                                   default_value=0.0,
                                   dtype=data_type)
        self._x_counter = 0

    def append_value(self, y_value):
        '''Appends the y value to the y_buffer and increments the sample
        number in the x_buffer
        '''
        self.y_buffer.append(y_value)
        self._x_counter += 1
        self.x_buffer.append(self._x_counter)

    def get_actual_filled_values(self):
        '''Gets the values from the buffer, which are already filled
        '''
        return self.x_buffer.partial, self.y_buffer.partial
