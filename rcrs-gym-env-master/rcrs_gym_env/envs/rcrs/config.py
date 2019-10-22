#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
config.py
v1.0 - 2/April/2018
Kevin Rodriguez Siu

This module mimics the function of the following classes:
rescuecore2.config.*

"""


#TO-DO Complete class Config based on rescuecore2.config.Config;

class Config:
    def __init__(self):
        self.data = {}
        # self.no_cache = {}
        # self.int_data = {}
        # self.float_data = {}
        # self.boolean_data = {}
        # self.array_data = {}

    def get_keys(self):
        return self.data.keys()

    def set_value(self, key, value):
        self.data[key] = value

    def get_value(self, key, default_value = None):
        if key not in self.data:
            return default_value
        else:
            return self.data.get(key)

