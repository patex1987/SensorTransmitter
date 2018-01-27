'''
Created on 24. 1. 2018
This module contains the class Sensor
This class can be used to simulate real life sensor. One can define minimum and
maximum value range and start random data generation (currently only a very
simple algorithm is generating the data). The value is generated by a
background thread - its either rising or decreasing.

@author: Patex
'''
import threading
import random
import time


class OutOfBoundException(Exception):
    '''Raised if the initial value is beyond the possible values of the sensors
    '''
    pass


class ThreadTerminatedException(Exception):
    '''Only for internal usage - Used to terminate background thread.
    '''
    pass


class Sensor(object):
    '''A class to generate random sensor data
    '''
    _max_stagnations = 7
    _max_movements = 7
    _stagnation_range = (-0.25, 0.25)
    _update_interval = 1

    def __init__(self,
                 min_value,
                 max_value,
                 unit,
                 move_range=(0.01, 1.0),
                 init_value=25):
        if init_value < min_value or init_value >= max_value:
            raise OutOfBoundException('Initial value out of bound')
        self._min_value = min_value
        self._max_value = max_value
        self.unit = unit
        self._move_range = move_range
        self._act_value = init_value
        self._direction = (-1)**random.randrange(2)
        self._thread_run_flag = False
        self._background_activity = threading.Thread(target=self._background_modification,
                                                     name='sensor_generation',
                                                     daemon=True)

    def run_data_generation(self):
        '''
        Runs the background thread for sensor data generation
        '''
        if self._background_activity.is_alive():
            return
        self._thread_run_flag = True
        self._background_activity.start()

    def stop_data_generation(self):
        '''
        Stops the background thread
        '''
        if not self._background_activity.is_alive():
            return
        self._thread_run_flag = False

    @property
    def actual_value(self):
        '''
        Property for getting the actual value
        '''
        return self._act_value

    def _background_modification(self):
        '''
        This method will be run in the background thread

        Continuously changes the value of the sensor. 2 changes are
        possible: 1. stagnation - fluctuation around the actual value
                  2. move - increase or decrease of the actual value, the
                     self_direction variable determines the direction of the
                     movement
        '''
        try:
            while True:
                self._repeated_change(self._max_stagnations,
                                      self._stagnation_range,
                                      False)
                self._repeated_change(self._max_movements,
                                      self._move_range,
                                      True)
        except ThreadTerminatedException as exit_thread:
            return

    def _repeated_change(self, max_cycles, value_range, can_change_direction):
        '''
        Increases or decreases the sensor value
        '''
        actual_cycles = random.randrange(1, max_cycles)
        for _ in range(actual_cycles):
            time.sleep(self._update_interval)
            if not self._thread_run_flag:
                raise ThreadTerminatedException
            act_change = random.uniform(value_range[0], value_range[1])
            self._change_value(amount=act_change,
                               can_change_direcion=can_change_direction)

    def _change_value(self, amount, can_change_direcion):
        '''
        Increments the sensor value
        '''
        new_value = self._act_value + (amount * self._direction)
        if not can_change_direcion:
            new_value = self._act_value + amount
        if new_value < self._min_value or new_value > self._max_value:
            if can_change_direcion:
                self._direction *= -1
            return
        self._act_value = new_value
