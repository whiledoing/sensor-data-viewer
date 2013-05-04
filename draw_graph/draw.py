#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

from numpy import *
import pylab as pl

from _parse_sensor_data import sensor_session

from _data_process import ave_filter

from quaterion import Quat
from quaterion import normalize


def load_session_file_dir():
    if len(sys.argv) < 2:
        print 'Input Session directory'
        return

    dir_name = sys.argv[1]
    if not os.path.exists(dir_name):
        print 'directory is not exist'
        return

    cur_dir = os.curdir
    all_file = os.listdir(dir_name)
    all_file.sort()

    os.chdir(dir_name)
    for f in os.listdir(all_file):
        if f.endswith('.xml'):
            show_acce_data(f)
    os.chdir(cur_dir)


def change_phy_to_soft(x, y, z):
    ''' change data from physical cordinate to software cordinate'''
    temp_x = x
    x = -y
    y = temp_x

    return (x, y, z)


def ave_f(data, ave_size):
    ave_data = data
    for i in range(0, min(len(data), ave_size)):
        ave_data[i] = mean(data[0:i+1])

    if len(data) <= ave_size:
        return ave_data

    for i in range(ave_size, len(data)):
        ave_data[i] = mean(data[i-ave_size+1:i+1])
    return ave_data


def get_sum_value(x, y, z):
    sum = zeros(len(x))

    for i in range(len(x)):
        sum[i] = sqrt(x[i]*x[i] + y[i]*y[i] + z[i]*z[i])

    return sum


def show_acce_data(file_name):
    try:
        session = sensor_session(file_name)
    except:
        print '[error loading session file] invalid session file : ' + file_name
        return

    # absolute file name
    file_name = os.path.abspath(file_name)

    # base file name
    file_base_name = os.path.splitext(os.path.basename(file_name))[0]

    # parent directory
    par_dir = os.path.dirname(file_name)

    # output directory
    dst_dir = par_dir + os.sep + "pic"

    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    filter_size = 3

    for sensor_id in session.get_ids():
        node_dir = dst_dir + os.sep + str(sensor_id)
        if not os.path.exists(node_dir):
            os.mkdir(node_dir)
        save_prefix = node_dir + os.sep + file_base_name + "_%s" + ".jpg"

        ax = array(session.get_specific_data_of_id(sensor_id, "Ax"), float64)
        ay = array(session.get_specific_data_of_id(sensor_id, "Ay"), float64)
        az = array(session.get_specific_data_of_id(sensor_id, "Az"), float64)
        (ax, ay, az) = change_phy_to_soft(ax, ay, az)

        sum_acce = get_sum_value(ax, ay, az)
        # sum_acce = variance_filter(sum_acce, 15)

        ax = ave_f(ax, filter_size)
        ay = ave_f(ay, filter_size)
        az = ave_f(az, filter_size)

        mx = array(session.get_specific_data_of_id(sensor_id, "Mx"), float64)
        my = array(session.get_specific_data_of_id(sensor_id, "My"), float64)
        mz = array(session.get_specific_data_of_id(sensor_id, "Mz"), float64)
        (mx, my, mz) = change_phy_to_soft(mx, my, mz)

        mx = ave_f(mx, filter_size)
        my = ave_f(my, filter_size)
        mz = ave_f(mz, filter_size)

        gx = array(session.get_specific_data_of_id(sensor_id, "Gx"), float64)
        gy = array(session.get_specific_data_of_id(sensor_id, "Gy"), float64)
        gz = array(session.get_specific_data_of_id(sensor_id, "Gz"), float64)

        (gx, gy, gz) = change_phy_to_soft(gx, gy, gz)
        sum_gyro = get_sum_value(gx, gy, gz)

        gx = ave_f(gx, filter_size)
        gy = ave_f(gy, filter_size)
        gz = ave_f(gz, filter_size)

        rw = array(session.get_specific_data_of_id(sensor_id, "Rw"), float64)
        rx = array(session.get_specific_data_of_id(sensor_id, "Rx"), float64)
        ry = array(session.get_specific_data_of_id(sensor_id, "Ry"), float64)
        rz = array(session.get_specific_data_of_id(sensor_id, "Rz"), float64)

        # rw = ave_filter(rw, filter_size)
        # rx = ave_filter(rx, filter_size)
        # ry = ave_filter(ry, filter_size)
        # rz = ave_filter(rz, filter_size)

        # total acce
        pl.figure(dpi=200)
        pl.plot(ave_filter(sum_acce, filter_size), label="TotalAcce", linewidth=1)
        pl.savefig(save_prefix % "TA", dpi=200)

        # total gyro
        pl.figure(dpi=200)
        pl.plot(ave_filter(sum_gyro, filter_size), label="TotalGyro", linewidth=1)
        pl.savefig(save_prefix % "TG", dpi=200)

        # acce
        pl.figure(dpi=200)
        pl.subplot(311)
        pl.plot(ax, label="Ax", color="r", linewidth=1)
        pl.subplot(312)
        pl.plot(ay, label="Ay", color="g", linewidth=1)
        pl.subplot(313)
        pl.plot(az, label="Az", color="b", linewidth=1)
        pl.savefig(save_prefix % "A", dpi=200)

        # magnetic
        pl.figure(dpi=200)
        pl.subplot(311)
        pl.plot(mx, label="Mx", color="r", linewidth=1)
        pl.subplot(312)
        pl.plot(my, label="My", color="g", linewidth=1)
        pl.subplot(313)
        pl.plot(mz, label="Mz", color="b", linewidth=1)
        pl.savefig(save_prefix % "M", dpi=200)

        # gyroscope
        pl.figure(dpi=200)
        pl.subplot(311)
        pl.plot(gx, label="Gx", color="r", linewidth=1)
        pl.subplot(312)
        pl.plot(gy, label="Gy", color="g", linewidth=1)
        pl.subplot(313)
        pl.plot(gz, label="Gz", color="b", linewidth=1)
        pl.savefig(save_prefix % "G", dpi=200)

        # euler anger
        pl.figure(dpi=200)

        q_yaw = zeros(len(rw))
        q_pitch = zeros(len(rw))
        q_roll = zeros(len(rw))

        for index in range(len(rw)):
            q = Quat(normalize([rx[index], ry[index], rz[index], rw[index]]))
            q_yaw[index] = q.ra
            q_pitch[index] = q.dec
            q_roll[index] = q.roll

        pl.subplot(311)
        pl.plot(q_yaw, label="yaw", linewidth=1)
        pl.subplot(312)
        pl.plot(q_pitch, label="pithch", linewidth=1)
        pl.subplot(313)
        pl.plot(q_roll, label="q_roll", linewidth=1)
        pl.savefig(save_prefix % "E", dpi=200)

        # quaterion
        pl.figure(dpi=200)
        pl.subplot(411)
        pl.plot(rw, label="Rw", linewidth=1)
        pl.subplot(412)
        pl.plot(rx, label="Rx", color="r", linewidth=1)
        pl.subplot(413)
        pl.plot(ry, label="Ry", color="g", linewidth=1)
        pl.subplot(414)
        pl.plot(rz, label="Rz", color="b", linewidth=1)

        pl.savefig(save_prefix % "R", dpi=200)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage Input : [xml file]"
        exit(-1)

    show_acce_data(sys.argv[1])
