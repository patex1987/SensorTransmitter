from PyQt4.QtCore import QThread, SIGNAL, QTimer
from ring_buffer import RingBuffer
import requests
from requests.exceptions import ConnectionError
import numpy as np


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
                #self.sleep(self.update_interval_secs)
                self.msleep(15)
            except NoDataError:
                self.emit(SIGNAL('handle_error()'))


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
