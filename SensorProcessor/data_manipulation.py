from PyQt4.QtCore import QThread, SIGNAL, QTimer
from ring_buffer import RingBuffer
import requests
from requests.exceptions import ConnectionError
import numpy as np
from collections import namedtuple
from datetime import datetime as dt


class NoDataError(Exception):
    '''This exception is raised if the data can't be retrieved from the API,
    or incorrect format is returned
    '''
    pass


class GetSensorsThread(QThread):
    '''This Thread is used to retrieve data from the API and sends them back
    to the main thread using Qt signals
    '''
    def __init__(self, start_thread=False, update_interval_secs=1):
        '''method constructor
        Args:
            start_thread (bool): a bool flag indicating whether the thread
                should be terminated
            update_interval_secs (int): interval between successive API
                requests. Expressed in seconds
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
                self.sleep(self.update_interval_secs)
            except NoDataError:
                self.emit(SIGNAL('handle_error()'))


class ProcessActuators(QThread):
    '''This thread processes the actual values of the sensors and compares
    them to the limit values, to calculate the actuator outputs
    
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
        '''method constructor

        Args:
            actual_temperature (number like): actual temperature value.
            actual_humidity (number like): actual humidity value.
            lower_temp_limit(number like): lower temperature limit for the
                heating.
            upper_temp_limit(number like): upper temperature limit for the
                cooling.
            humidity_limit(number like): optimal humidity level
            min_voltage(number like): minimum possible voltage level of the
                ventilation
            max_voltage(number like): maximum possible voltage level of the
                ventilation
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
        Actuators = namedtuple('Actuators',
                               'heating cooling ventilation')
        heating = int(self._actual_temperature < self._lower_temp_limit)
        cooling = int(self._actual_temperature > self._upper_temp_limit)
        ventilation = self._calculate_ventilation_state()
        actual_actuators = Actuators(heating=heating,
                                     cooling=cooling,
                                     ventilation=ventilation)
        self.emit(SIGNAL('actuator_values(PyQt_PyObject)'),
                  actual_actuators)

    def _calculate_ventilation_state(self):
        '''Based on linear regression calculates the voltage of the
        ventilation. Linear regression: y=a*x+b
        
        Returns the output voltage of the ventilation based on the humidity
        level
        '''
        if self._actual_humidity < self._humidity_limit:
            return 0       
        volt_diff = self._max_voltage - self._min_voltage
        humid_diff = 100 - self._humidity_limit
        coeff_a = volt_diff / humid_diff
        coeff_b = self._min_voltage - (coeff_a*self._humidity_limit)
        output_voltage = (coeff_a*self._actual_humidity) + coeff_b
        return output_voltage
        


class XYBuffer(object):
    '''A class for holding X and Y about the sensor

    Basically a ring buffer, which serves as the data input for plotting
    sensor values as a moving windows in pyqtgraph
    '''
    def __init__(self,
                 update_interval_secs,
                 total_secs=3600,
                 data_type=float):
        '''XYBuffer constructor

        Args:
            update_interval_secs (int): How often is the pyqtgraph updated
            total_secs (int): What's the maximum length of the moving window.
                Default size 3600 seconds - i.e. 1 hour
            data_type(): use numpy data types
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
        '''Appends the y_value to the y_buffer and increments the sample
        number in the x_buffer
        '''
        self.y_buffer.append(y_value)
        self._x_counter += 1
        self.x_buffer.append(self._x_counter)

    def get_actual_filled_values(self):
        '''Gets the values from the buffer, which are already filled
        
        Used for data plotting
        '''
        return self.x_buffer.partial, self.y_buffer.partial
