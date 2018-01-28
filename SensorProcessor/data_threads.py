from PyQt4.QtCore import QThread, SIGNAL, QTimer
from ring_buffer import RingBuffer
import requests
from requests.exceptions import ConnectionError
import numpy as np

class NoDataError(Exception):
    pass

class GetSensorsThread(QThread):
    def __init__(self, start_thread=False, update_interval=1):
        '''
        method constructor
        '''
        super().__init__()
        self.start_thread = start_thread
        self.update_interval = update_interval

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
                #print('IN THREAD')
                self.sleep(self.update_interval)
            except NoDataError:
                self.emit(SIGNAL('handle_error()'))
