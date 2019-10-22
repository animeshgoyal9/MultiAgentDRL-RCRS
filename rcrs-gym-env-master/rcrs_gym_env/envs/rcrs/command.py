#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
command.py
v1.0 - 9/April/2018
Kevin Rodriguez Siu

This module mimics the function of the following classes:
rescuecore2.messages.Command

"""

from message import Message
from world_model import EntityID

class Command(Message):
     
    def __init__(self, nid = 0, ntime = 0):
        self.agent_id = EntityID(nid)
        self.time = ntime
    
    def get_agent_id(self):
        return self.agent_id
    
    def get_time(self):
        return self.time