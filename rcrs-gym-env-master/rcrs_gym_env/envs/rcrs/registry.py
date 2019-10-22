#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
registry.py
v1.0 - 19/March/2018
Kevin Rodriguez Siu

This module mimics the function of the rescuecore2.registry.Registry class

"""
import warnings
from threading import local

class Registry():
    
    SYSTEM_REGISTRY = "System"
    CURRENT_REGISTRY = local()
    parent = None
    name = None
    entity_factories = None
    property_factories = None
    message_factories = None
    
    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent
        self.entity_factories = {}
        self.property_factories = {}
        self.message_factories = {}
        
    def get_current_registry(self):
        return self.CURRENT_REGISTRY
    
    def set_current_registry(self, r):
        if r.isinstance(Registry):
            self.CURRENT_REGISTRY = r
            return True
        return False
    
    def to_string(self):
        return self.getName()
    
    def get_name(self):
        if self.name is None:
            return super.toString()
        return self.name
    
    def create_property(self, urn):
        factory = self.getPropertyFactory(urn)
        
        if factory is None:
            message = self.getName() + ": Property " + urn + " not recognized."
            warnings.warn(message,RuntimeWarning)
            return None
        return factory.makeProperty(urn)
    
    def get_property_factory(self,urn):
        result = None
        result = self.property_factories.get(urn)  #TO-DO: Synchronized way
        if result is None and not (self.parent is None):
            result = self.parent.getPropertyFactory(urn)
        return result 
        
        
    def create_entity(self, urn, eid):
        factory = self.getEntityFactory(urn)
        if factory is None:
            message = self.getName() + ": Entity " + urn + " not recognized."
            warnings.warn(message,RuntimeWarning)
            return None
        return factory.makeEntity(urn,id)
    
    def get_entity_factory(self, urn):
        result = None
        result = self.entity_factories.get(urn) #TO-DO: Synchronized way
        if result is None and not (self.parent is None):
            result = self.parent.getEntityFactory(self,urn)
        return result