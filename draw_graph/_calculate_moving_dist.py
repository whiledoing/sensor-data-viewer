# -*- coding: utf-8 -*-
# Filename: my_calculation.py

from numpy import *


def calculate_moving_dist(ave_x, ave_y, ave_z, moving_data):
    ''' ave_x,y,z 表示三轴静止状态下的平均值
    moving_data表示移动的传感器数据，注意数据都是去掉了重力的影响的
    '''
    # 采样时间
    t = 0.033

    # 计算垂直方向加速度（假设这里给出的是x的加速度）
    theta = arctan(ave_y/ave_x)
    acce = moving_data/cos(theta)

    # 速度
    v = zeros(len(acce))
    for i in range(1, len(acce)):
        v[i] = v[i-1] + ((acce[i] + acce[i-1])/2)*t

    # mandantory change the last value to be zero
    v[len(v)-1] = 0

    # 距离
    dist = 0.0
    for i in range(1, len(v)):
        dist += ((v[i] + v[i-1])/2)*t;

    return dist


def walk_dist(vertical_dist, leg_len):
    if vertical_dist < 0:
        vertical_dist = -vertical_dist
    dist = sqrt(leg_len**2 - (leg_len-vertical_dist)**2)
    return dist*2


if __name__ == '__main__':
    still_data = [(1.125, 0.015625, 0.296875), (1.093750,-0.015625,0.312500),
            (1.093750,-0.015625,0.296875),(1.09375,0.0,0.343750)]

    moving_data = [(1.015625, 0.0, 0.453125), (1.093750,0.046875,0.375000),
            (1.25,0.0625,0.5),(1.609375,-0.078125,0.5625),
            (1.5,-0.015625,0.609375), (1.609375,0.078125,0.265625),
            (1.46875,0.109375,-0.25),(0.921875,-0.171875,-0.140625),
            (0.765625, -0.078125, 0.312500),(1.078125,0.156250,0.390625),
            (0.984375,0.078125,0.0625)]

    still_data = array(still_data, float64)
    moving_data = array(moving_data, float64)

    ave_x = mean(still_data[:, 0])
    ave_y = mean(still_data[:, 1])
    ave_z = mean(still_data[:, 2])

    # 去掉重力的影响
    moving_data -= (ave_x, ave_y, ave_z)

    # 腿长
    leg_len = 1.10

    # 步行移动的距离（这里使用第一列的元素）
    dist = calculate_moving_dist(ave_x, ave_y, ave_z, moving_data[:, 0])
    print "moving distance is", walk_dist(dist, leg_len)
