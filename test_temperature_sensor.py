'''
Created on 24. 1. 2018

@author: Patex
'''
import pytest
from sensor_generator import TemperatureSensor, OutOfBoundException


@pytest.fixture
def sensor():
    '''
    returns a basic TemperatureSensor object
    '''
    return TemperatureSensor()


def incrementer(init_direction, init_temp, increment_value):
    sensor._direction = init_direction
    sensor._act_temp = init_temp
    sensor._increment_temp(increment_value, False)
    return sensor.actual_temperature
    

def test_actual_value(sensor):
    '''
    Tests if a sensor contains an _act_temperature member
    '''
    assert isinstance(sensor._act_temp, int)
    assert sensor._act_temp >= TemperatureSensor._min_temp
    assert sensor._act_temp <= TemperatureSensor._max_temp


def test_outofbound_raises():
    '''
    Checks if exception is raised, when the class is initialized with wrong
    temperature
    '''
    with pytest.raises(OutOfBoundException):
        TemperatureSensor(init_temp=-25)


def test_movement_direction(sensor):
    '''
    checks if sensor movement direction is created correctly
    '''
    assert sensor._direction in (-1, 1)


def test_temperature_property(sensor):
    '''
    Checks if the actual_temperature property works correctly
    '''
    assert sensor.actual_temperature == sensor._act_temp


def test_increment(sensor):
    '''
    Checks if _increment_temp() works correctly
    '''
    test_sets = ((1, 25, 0.5, 25.5),
                 (1, 50, 10, 60),
                 (1, 78, 6, 78),
                 (1, 12, -10, 12))
    for test_set in test_sets:
        new_value = incrementer(*test_set[:-1])
        assert new_value == test_set[-1]

def test_increment_with_direction_change(sensor):
    '''
    Checks if increment changes the movement direction if the temperature
    value reaches the limit of the possible values
    '''
    sensor._direction = 1
    sensor._act_temp = 78
    sensor._increment_temp(10, True)
    sensor._increment_temp(10, True)
    assert sensor.actual_temperature == 68