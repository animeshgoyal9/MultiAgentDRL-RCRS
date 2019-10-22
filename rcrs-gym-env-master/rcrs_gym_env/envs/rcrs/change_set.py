# -*- coding: utf-8 -*-
"""
change_set.py
v1.0 - 19/March/2018
Kevin Rodriguez Siu

This module mimics the function of the rescuecore2.worldmodel.ChangeSet class

"""

import encoding_tool as et
import world_model as wm


class ChangeSet:
    def __init__(self, _change_set = None):
        self.deleted = set()
        self.changed = {}
        self.entity_urns = {}
        if _change_set is not None:
            self.merge(_change_set)

    def add_change(self, entity, property):
        # print('add_change 1:' + str(type(entity.get_id())))
        self.add_change(entity.get_id(), entity.get_urn(), property)

    def add_change(self, entity_id, entity_urn, property):
        # print('add_change 2:' + str(type(entity_id)))
        if entity_id in self.deleted:
            return

        new_property = property.copy()
        property_dict = {}
        if self.changed.has_key(entity_id):
            property_dict = self.changed.get(entity_id)

        property_dict[new_property.get_urn()] = new_property
        self.changed[entity_id] = property_dict
        self.entity_urns[entity_id] = entity_urn
    
    def entity_deleted(self, _entity_id):
        self.deleted.add(_entity_id)
        if _entity_id in self.changed:
            del self.changed[_entity_id]
        
    def get_changed_properties(self, _entity_id):
        if self.changed.has_key(_entity_id):
            return self.changed[_entity_id].values()
        return []
    
    def get_changed_property(self, _entity_id, prop_urn):
        if self.changed.has_key(_entity_id):
            property_dict = self.changed.get(_entity_id)
            if property_dict is not None and len(property_dict) > 0:
                if property_dict.has_key(prop_urn):
                    return property_dict[prop_urn]
        return None
    
    def get_changed_entities(self):
        return self.changed.keys()
    
    def get_deleted_entities(self):
        return self.deleted
    
    def get_entity_urn(self, _entity_id):
        return self.entity_urns.get(_entity_id)
    
    def merge(self, _change_set):
        for _entity_id in _change_set.changed:
            _entity_urn = _change_set.get_entity_urn(_entity_id)
            _property_dict = _change_set.changed[_entity_id]
            for _property_urn in _property_dict:
                self.add_change(_entity_id, _entity_urn, _property_dict[_property_urn])

        for _entity_id in _change_set.deleted:
            self.entity_deleted(_entity_id)
    
    # def add_all(self, c):
    #     for elem in c:
    #         if elem.isinstance(Entity):
    #             for p in elem.get_properties():
    #                 if p.is_defined():
    #                     self.add_change(elem,p)
    #     return
    
    def write(self, output_stream):
        et.write_int32(len(self.changed), output_stream)
        for entity_id in self.changed:
            et.write_int32(entity_id.get_value(), output_stream)
            et.write_str(self.get_entity_urn(entity_id), output_stream)

            properties = self.changed[entity_id].values()
            et.write_int32(len(properties), output_stream)
            for property in properties:
                et.write_property(property, output_stream)

        et.write_int32(len(self.deleted), output_stream)
        for entity_id in self.deleted:
            et.write_int32(entity_id.get_value(), output_stream)

    def read(self, input_stream):
        self.changed.clear()
        self.deleted.clear()
        self.entity_urns.clear()
        
        entity_count = et.read_int32(input_stream)
        for i in range(entity_count):
            entity_id = wm.EntityID(et.read_int32(input_stream))
            entity_urn = et.read_str(input_stream)
            property_count = et.read_int32(input_stream)
            for j in range(property_count):
                property = et.read_property(input_stream)
                if property is not None:
                    self.add_change(entity_id, entity_urn, property)

        deleted_count = et.read_int32(input_stream)
        for i in range(deleted_count):
            entity_id = wm.EntityID(et.read_int32(input_stream))
            self.entity_deleted(entity_id)
    
    def to_string(self):
        result = ""
        result += "change_set:"
        #TO-DO: Complete toString features
        return result 
    
    def debug(self):
        result = ""
        #TO-DO: Complete Debug features
        return result
        
            
        
        
                
            
    
    
            
    
    
        
    