#!/usr/bin/python
# Filename: _data_process.py

from numpy import average
from numpy import zeros
from numpy import abs


def ave_filter_of_index(sensor_data, index, filter_size):
    assert(index >= 0 and index < len(sensor_data))
    assert(filter_size >= 0)

    left_index = max(0, index - filter_size)
    right_index = min(index + filter_size + 1, len(sensor_data))

    return average(sensor_data[left_index : right_index])


def ave_filter(sensor_data, filter_size):
    result = zeros(len(sensor_data))
    for i in range(0, len(sensor_data)):
        result[i] = ave_filter_of_index(sensor_data, i, filter_size)
    return result


def variance_data_of_index(sensor_data, index, filter_size):
    assert(index >= 0 and index < len(sensor_data))
    assert(filter_size >= 0)

    left_index = max(0, index - filter_size)
    right_index = min(index + filter_size + 1, len(sensor_data))

    range_data = sensor_data[left_index : right_index]
    mean_value = average(range_data)

    for i in range(0, len(range_data)):
        range_data[i] = (range_data[i] - mean_value)**2

    return average(range_data)


def variance_filter(sensor_data, filter_size):
    result = zeros(len(sensor_data))
    for i in range(0, len(sensor_data)):
        result[i] = variance_data_of_index(sensor_data, i, filter_size)
    return result


def get_max_abs_index(data):
    max_value = -1.0
    max_index = -1
    for i in range(len(data)):
        if abs(data[i]) > max_value:
            max_value = abs(data[i])
            max_index = i

    return max_index


def get_extreme_point(sensor_data, delta=0.0):
    points = list()
    values = list()

    # find the extreme point and remove value less than delta
    for i in range(1, len(sensor_data)-1):
        if abs(sensor_data[i]) >= abs(sensor_data[i-1]):
            if abs(sensor_data[i]) >= abs(sensor_data[i+1]):
                if abs(sensor_data[i]) >= abs(delta):
                    points.append(i)
                    values.append(sensor_data[i])

    if len(points) <= 1:
        return (points, values)

    sign_value = values[0]
    use_points = list()
    use_values = list()
    i = 0
    while i < len(values):
        temp_value = list()
        while i < len(values) and values[i]*sign_value > 0:
            temp_value.append(values[i])
            i += 1
        max_index = get_max_abs_index(temp_value)
        if max_index != -1:
            max_index = i - (len(temp_value)-max_index)
            use_points.append(points[max_index])
            use_values.append(values[max_index])

        temp_value = list()
        while i < len(values) and values[i]*sign_value <= 0:
            temp_value.append(values[i])
            i += 1
        max_index = get_max_abs_index(temp_value)
        if max_index != -1:
            max_index = i - (len(temp_value)-max_index)
            use_points.append(points[max_index])
            use_values.append(values[max_index])

    return (use_points, use_values)
    # return (points, values)
