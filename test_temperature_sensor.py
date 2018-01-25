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


def incrementer(sensor, init_direction, init_temp, increment_value, change_direction):
    sensor._direction = init_direction
    sensor._act_temp = init_temp
    sensor._increment_temp(increment_value, change_direction)
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


def test_increment_wo_direction_change(sensor):
    '''
    Checks if _increment_temp() works correctly. I.e. returns expected values,
    and doesnt change the direction, if can_change_direction is set to False
    '''
    test_sets = ((1, 25, 0.5, 25.5),
                 (1, 50, 10, 60),
                 (1, 78, 6, 78),
                 (1, 12, -10, 12))
    for test_set in test_sets:
        new_value = incrementer(sensor=sensor,
                                init_direction=test_set[0],
                                init_temp=test_set[1],
                                increment_value=test_set[2],
                                change_direction=False)
        assert new_value == test_set[3]
        assert sensor._direction == test_set[0]


def test_increment_with_direction_change(sensor):
    '''
    Checks if increment changes the movement direction if the temperature
    value reaches the limit of the possible values
    '''
    def make_multiple_temp_changes(init_direction, init_temp, change_sets):
        sensor._direction = init_direction
        sensor._act_temp = init_temp
        for change_set in change_sets:
            new_value = incrementer(sensor=sensor,
                                    init_direction=sensor._direction,
                                    init_temp=sensor.actual_temperature,
                                    increment_value=change_set[0],
                                    change_direction=True)
            assert change_set[1] == sensor._direction
            assert change_set[2] == sensor.actual_temperature
    
    test_sets = ((1, 78, [[3, -1, 78], [3, -1, 75]]),
                 (-1, 25, [[3, -1, 22], [3, 1, 22], [3, 1, 25]]))
    for test_set in test_sets:
        make_multiple_temp_changes(*test_set)

def test_repeated_change(sensor):
    '''
    Tests if _repeated_change() changes temperature value properly (after
    applying multiple changes)
    
    Note: Here, we are not testing cases, where the direction changes during the movement
    '''
    def check_repeated_change(init_direction, init_temp, max_cycles, value_range):
        sensor._direction = init_direction
        sensor._act_temp = init_temp
        sensor._thread_close_flag = True
        sensor._repeated_change(max_cycles=max_cycles, value_range=value_range, can_change_direction=False)
        new_temp = sensor.actual_temperature
        expected_minimum = init_temp + value_range[0]
        expected_maximum = init_temp + (value_range[1] * (max_cycles - 1))
        
        assert new_temp >=  expected_minimum and new_temp <= expected_maximum
    
    test_sets = ((1, 25, 2, (2, 2)),
                 (1, 25, 4, (2, 10)))
    for test_set in test_sets:
        check_repeated_change(*test_set)
