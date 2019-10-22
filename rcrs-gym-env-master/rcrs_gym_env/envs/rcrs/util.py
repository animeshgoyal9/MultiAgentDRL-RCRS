import sys, math


def print_bytes(byte_array):
    for val in byte_array:
        sys.stdout.write(str(ord(val)) + ' ')
    sys.stdout.flush()


def cal_distance(p1x, p1y, p2x, p2y):
    return math.hypot(p1x-p2x, p1y-p2y)

