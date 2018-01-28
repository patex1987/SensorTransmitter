'''
Created on 24. 1. 2018

@author: Patex
'''
import time
import datetime as dt
import pytest
from sensor_generator import Sensor, OutOfBoundException


@pytest.fixture
def sensor():
    '''
    returns a basic TemperatureSensor object
    '''
    return Sensor(min_value=20,
                  max_value=80,
                  unit='C',
                  move_range=(0.01, 1.0),
                  init_value=25)


def incrementer(sensor,
                init_direction,
                init_value,
                amount,
                change_direction):
    '''
    increments the value of the sensor
    '''
    sensor._direction = init_direction
    sensor._act_value = init_value
    sensor._change_value(amount, change_direction)
    return sensor.actual_value


def test_actual_value(sensor):
    '''
    Tests if a sensor contains an _act_value member
    '''
    assert isinstance(sensor._act_value, int)
    assert sensor._act_value >= sensor._min_value
    assert sensor._act_value <= sensor._max_value


def test_outofbound_raises():
    '''
    Checks if exception is raised, when the class is initialized with wrong
    initial value
    '''
    with pytest.raises(OutOfBoundException):
        Sensor(min_value=20,
               max_value=80,
               unit='C',
               move_range=(0.01, 1.0),
               init_value=-25)


def test_movement_direction(sensor):
    '''
    checks if sensor movement direction is created correctly
    '''
    assert sensor._direction in (-1, 1)


def test_value_property(sensor):
    '''
    Checks if the actual_value property works correctly
    '''
    assert sensor.actual_value == sensor._act_value


def test_increment_wo_direction_change(sensor):
    '''
    Checks if _change_value() works correctly. I.e. returns expected values,
    and doesn't change the direction, if can_change_direction is set to False
    '''
    test_sets = ((1, 25, 0.5, 25.5),
                 (1, 50, 10, 60),
                 (1, 78, 6, 78),
                 (1, 12, -10, 12))
    for test_set in test_sets:
        new_value = incrementer(sensor=sensor,
                                init_direction=test_set[0],
                                init_value=test_set[1],
                                amount=test_set[2],
                                change_direction=False)
        assert new_value == test_set[3]
        assert sensor._direction == test_set[0]


def test_increment_with_direction_change(sensor):
    '''
    Checks if increment changes the movement direction if the sensor
    value reaches the limit of the possible values
    '''
    def make_multiple_value_changes(init_direction, init_value, change_sets):
        sensor._direction = init_direction
        sensor._act_value = init_value
        for change_set in change_sets:
            new_value = incrementer(sensor=sensor,
                                    init_direction=sensor._direction,
                                    init_value=sensor.actual_value,
                                    amount=change_set[0],
                                    change_direction=True)
            assert change_set[1] == sensor._direction
            assert change_set[2] == new_value

    test_sets = ((1, 78, [[3, -1, 78], [3, -1, 75]]),
                 (-1, 25, [[3, -1, 22], [3, 1, 22], [3, 1, 25]]))
    for test_set in test_sets:
        make_multiple_value_changes(*test_set)


def test_repeated_change(sensor):
    '''
    Tests if _repeated_change() changes sensor value properly (after
    applying multiple changes)

    Note: Here, we are not testing cases, where the direction changes during
    the movement
    '''
    def check_repeated_change(init_direction,
                              init_value,
                              max_cycles,
                              value_range):
        sensor._direction = init_direction
        sensor._act_value = init_value
        sensor._thread_run_flag = True
        sensor._repeated_change(max_cycles=max_cycles,
                                value_range=value_range,
                                can_change_direction=False)
        new_value = sensor.actual_value
        expected_minimum = init_value + value_range[0]
        expected_maximum = init_value + (value_range[1] * (max_cycles - 1))

        assert new_value >= expected_minimum and new_value <= expected_maximum

    test_sets = ((1, 25, 2, (2, 2)),
                 (1, 25, 4, (2, 10)))
    for test_set in test_sets:
        check_repeated_change(*test_set)


def test_stagnation(sensor):
    '''
    Tests if during the stagnation type of change the sensor value doesnt
    change too much
    '''
    sensor._update_interval = 0.01
    for _ in range(10):
        sensor._act_value = 79.95
        sensor._thread_run_flag = True
        sensor._repeated_change(max_cycles=10,
                                value_range=(-0.2, 0.2),
                                can_change_direction=False)
        end_value = sensor.actual_value
        assert end_value >= 77.95 and end_value < 80


def test_running_thread(sensor):
    '''
    Tests if background thread is running and terminating properly, and
    whether it is changing the value

    Here we are testing multiple things:
    1 - if we start the continuous modification of the sensor value, the
        background thread should be alive
    2 - once we stop the background thread, the is_alive() method should return
        False
    3 - after running a couple of cycles, the sensor's value should be
        different than the initial value
    4 - if we stop the background thread, the actual modification cycle should
        be finished, i.e. the closing time of the thread should be less than
        2 * update interval
    '''
    sensor._act_value = 25
    sensor._update_interval = 0.01
    sensor._stagnation_range = (0.1, 0.25)
    sensor.run_data_generation()
    assert sensor._background_activity.is_alive()
    time.sleep(2*sensor._update_interval)
    sensor.stop_data_generation()
    last_thread_timestamp = dt.datetime.now()
    sensor._background_activity.join()
    exited_thread = dt.datetime.now()
    exit_duration = exited_thread - last_thread_timestamp
    assert not sensor._background_activity.is_alive()
    assert sensor.actual_value != 25
    assert exit_duration.total_seconds() < 2*sensor._update_interval
