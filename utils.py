import struct

import binascii

import time
from direct.stdpy import threading
# import threading
# from lxml import etree

import numpy as num
from panda3d.core import LVector3f, LVector4f, Vec3, LVector3i


def vecf_to_veci(vector):
    return LVector3f(vector.x, vector.y, vector.z)


def to_vec3i(vector):
    return LVector3i(floor(vector.x), floor(vector.y), floor(vector.z))


def add_list(vector, array):
    if isinstance(array, list):
        return [vector + element for element in array]
    return None


def floor(x):
    return int(num.floor(x))


def string_to_number(string):
    string = string.strip()
    try:
        return int(string)
    except ValueError:
        try:
            return float(string)
        except ValueError:
            return string


def hex_to_normalized_rgb(hex_color):
    r, g, b = struct.unpack('BBB', bytes.fromhex(hex_color.lstrip('#')))
    return r/255, g/255, b/255


def normalized_rgb_to_hex(color):
    return '#' + binascii.hexlify(struct.pack('BBB', int(color.x*255), int(color.y*255), int(color.z*255))).decode("utf-8")


class SafeThread(threading.Thread):
    def __init__(self, func, param, end_function):
        threading.Thread.__init__(self)
        self.daemon = True
        self.Finish = 0
        self.Func = func
        self.Param = param
        self.end_function = end_function

    def run(self):
        self.Func(*self.Param)

        self.Finish = 1
        self.join()
        self.end_function()


class ThreadQueue:
    def __init__(self):
        self._threads = []

    # def _compose(self, func, *args):
    #     print('calling ', func.__str__())
    #     func.__call__(*args)
    #     print('ending.')
    #     self._start_next()

    def new_thread(self, function, *args):
        print('adding a new thread while size = ', len(self._threads))
        self._threads.append(SafeThread(func=function, param=(*args, ), end_function=self._start_next))
        if len(self._threads) == 1:
            self._threads[0].start()
    #
    # def _start_thread(self):
    #     if len(self._threads) > 0:
    #         self._threads[0].start()

    def _start_next(self):
        if len(self._threads) > 0:
            old = self._threads.pop(0)
            if len(self._threads) > 0:
                self._threads[0].start()
            else:
                print('ending all threads !')


class NameFormatter:
    @staticmethod
    def generate_name(base_name, pos):
        return base_name + '.' + str(int(pos.x)) + '.' + str(int(pos.y)) + '.' + str(int(pos.z))

    @staticmethod
    def get_pos(name):
        return LVector3i(int(name.split('.')[1]), int(name.split('.')[2]), int(name.split('.')[3]))

    @staticmethod
    def get_object_name(name):
        return name.split('.')[0]
