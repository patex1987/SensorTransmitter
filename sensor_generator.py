'''
Created on 24. 1. 2018
This module contains the class Sensor
This class can be used to simulate real life sensor. One can define minimum and
maximum temperature range and random value generation. Currently only a very
simple algorithm is implemented. The sensor value is either rising decreasing.
A background thread is modifying the sensor's value

@author: Patex
'''
import threading
import random
import time


class OutOfBoundException(Exception):
    '''Raised if the initial value is beyondd the possible values of the sensors
    '''
    pass


class ThreadTerminatedException(Exception):
    '''Only for internal usage - Used to terminate background thread.
    '''
    pass


class TemperatureSensor(object):
    '''A class to generate random sensor data
    '''
    _min_temp = 20
    _max_temp = 80
    _max_stagnations = 7
    _max_movements = 7
    _stagnation_range = (-0.25, 0.25)
    _move_range = (0.01, 1.0)
    _update_interval = 1

    def __init__(self, init_temp=25):
        if init_temp < self._min_temp or init_temp >= self._max_temp:
            raise OutOfBoundException('Initial temperature out of bound')
        self._act_temp = init_temp
        self._direction = (-1)**random.randrange(2)
        self._thread_close_flag = False
        self._background_activity = threading.Thread(target=self._background_modification,
                                                     name='sensor_generation',
                                                     daemon=True)

    def run_data_generation(self):
        '''
        Runs the background thread for sensor data generation
        '''
        if self._background_activity.is_alive():
            return
        self._thread_close_flag = True
        self._background_activity.start()

    def stop_data_generation(self):
        '''
        Stops the background thread
        '''
        if not self._background_activity.is_alive():
            return
        self._thread_close_flag = False

    @property
    def actual_temperature(self):
        '''
        Property for getting the actual temperature
        '''
        return self._act_temp

    def _background_modification(self):
        '''
        This method will be run in the background thread

        Continuously changes the value of the temperature. 2 changes are
        possible: 1. stagnation - fluctuation around the actual temperature
                  2. move - increase or decrease of the actual temperature, the
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
        except ThreadTerminatedException as e:
            return

    def _repeated_change(self, max_cycles, value_range, can_change_direction):
        '''
        Increases or decreases the temperature value
        '''
        actual_cycles = random.randrange(1, max_cycles)
        for _ in range(actual_cycles):
            time.sleep(self._update_interval)
            if not self._thread_close_flag:
                raise ThreadTerminatedException
            act_change = random.uniform(value_range[0], value_range[1])
            self._increment_temp(temp_change=act_change,
                                 can_change_direcion=can_change_direction)

    def _increment_temp(self, temp_change, can_change_direcion):
        '''
        Increments the temperature value
        '''
        new_value = self._act_temp + (temp_change * self._direction)
        if not can_change_direcion:
            new_value = self._act_temp + temp_change
        if new_value < self._min_temp or new_value > self._max_temp:
            if can_change_direcion:
                self._direction *= -1
            return
        self._act_temp = new_value
