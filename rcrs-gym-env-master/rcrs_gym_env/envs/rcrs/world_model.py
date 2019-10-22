#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
world_model.py
v1.0 - 19/March/2018
Kevin Rodriguez Siu

This module mimics the function of the following classes:
rescuecore2.worldmodel.Entity
rescuecore2.worldmodel.EntityID
rescuecore2.worldmodel.Property

"""
import urn
import property as p
import encoding_tool as et
import entity_factory as ef
import world_model as wm
from rtree import index
import sys


class WorldModel():
    def __init__(self):
        self.entities = {}
        self.indexed = False
        self.index = index.Index()
        self.human_rectangles = {}
        self.minx = None
        self.miny = None
        self.maxx = None
        self.maxy = None

    def add_entities(self, _entities):
        for entity in _entities:
            self.entities[entity.get_id()] = entity

    def get_entity(self, entity_id):
        # print('get_entity 3:' + str(type(entity_id)))
        # for entity_id_ in self.entities:
        #     print(str(entity_id_.get_value()))
        if entity_id in self.entities:
            return self.entities.get(entity_id)
        else:
            # print('not found entity_id:' + str(entity_id.get_value()))
            return None

    def add_entity(self, entity):
        self.entities[entity.get_id()] = entity

    def remove_entity(self, entity_id):
        del self.entities[entity_id]

    def merge(self, change_set):
        for entity_id in change_set.get_changed_entities():
            existing_entity = self.get_entity(entity_id)
            added = False
            if existing_entity is None:
                existing_entity = ef.create_entity(entity_id, change_set.get_entity_urn(entity_id))
                if existing_entity is None:
                    print('world model merge existing entity is still None')
                    continue
                added = True

            for property in change_set.get_changed_properties(entity_id):
                existing_property = existing_entity.get_property(property.get_urn())
                existing_property.take_value(property)

            if added:
                self.add_entity(existing_entity)

        for entity_id in change_set.get_deleted_entities():
            self.remove_entity(entity_id)

        #update human rectangles
        new_human_rectangles_to_push = {}
        for human, rectangle in self.human_rectangles.iteritems():
            self.index.delete(human.get_id().get_value(), rectangle)
            left, bottom, right, top = self.make_rectangle(human)
            if left is not None:
                self.index.insert(human.get_id().get_value(), (left, bottom, right, top))
                new_human_rectangles_to_push[human] = (left, bottom, right, top)

        for human, rectangle in new_human_rectangles_to_push:
            self.human_rectangles[human] = rectangle

    def index(self):
        if not self.indexed:
            self.minx = sys.maxint
            self.miny = sys.maxint
            self.maxx = sys.minint
            self.maxy = sys.minint

            self.index = index.Index()
            self.human_rectangles.clear()

            for entity in self.entities.values():
                left, bottom, right, top = self.make_rectangle(entity)
                if left is not None:
                    self.index.insert(entity.get_id().get_value(), (left, bottom, right, top))
                    self.minx = min(self.minx, left, right)
                    self.maxx = max(self.maxx, left, right)
                    self.miny = min(self.miny, bottom, top)
                    self.maxy = max(self.maxy, bottom, top)
                    if isinstance(entity, Human):
                        self.human_rectangles[entity] = (left, bottom, right, top)
            self.indexed = True

    def make_rectangle(self, entity):
        x1 = sys.maxint
        x2 = sys.minint
        y1 = sys.maxint
        y2 = sys.minint
        apexes = None
        if isinstance(entity, Area):
            apexes = entity.get_apexes()
        elif isinstance(entity, Blockade):
            apexes = entity.get_apexes()
        elif isinstance(entity, Human):
            apexes = []
            human_x, human_y = entity.get_location(self)
            apexes.append(human_x)
            apexes.append(human_y)
        else:
            return None, None, None, None

        if len(apexes) == 0:
            print('this area, blockade or human entity does not have apexes!!')
            return None
        for i in range(0, len(apexes), 2):
            x1 = min(x1, apexes[i])
            x2 = max(x2, apexes[i])
            y1 = min(y1, apexes[i+1])
            y2 = max(y2, apexes[i+1])
        return x1, y1, x2, y2

    def get_entities(self):
        return self.entities.values()


class EntityID:
    def __init__(self, _id):
        self.id = _id
        
    def __eq__(self, other):
        if isinstance(other, EntityID):
            return self.id == other.id
        return False

    def __hash__(self):
        return self.id
    
    def get_value(self):
        return self.id
    
    def __str__(self):
        return str(self.id)
        

class Edge():
    def __init__(self, start_x, start_y, end_x, end_y, _neighbor):
        self.start = [start_x, start_y]
        self.end = [end_x, end_y]
        self.line = [[start_x, start_y], [end_x, end_y]]
        self.neighbor = _neighbor

    def get_start_x(self):
        return self.start[0]

    def get_start_y(self):
        return self.start[1]

    def get_end_x(self):
        return self.end[0]

    def get_end_y(self):
        return self.end[1]

    def get_neighbor(self):
        return self.neighbor


class Entity:
    def __init__(self, _entity_id):
        self.entity_id = _entity_id
        self.properties = {}
    
    def add_entity_listener(self,l):
        pass
    
    def remove_entity_listener(self,l):
        pass
    
    def get_id(self):
        return self.entity_id
    
    def get_properties(self):
        return self.properties
    
    def get_property(self, prop_urn):
        return self.properties[prop_urn]

    def get_location(self, world_model):
        # returns the position of the entity on the world model
        pass

    def register_properties(self, props):
        for p in props:
            self.properties[p.get_urn()] = p

    def write(self, out):
        count = 0
        for p in self.properties:
            if p.is_defined():
                count += 1
        et.write_int32(count, out)
        for p in self.properties:
            if p.is_defined():
                et.write_property(p, out)
    
    def read(self, inp):
        count = et.read_int32(inp)
        for i in range(count):
            p = et.read_property(inp)
            # print('property value:' + str(p.get_value()))
            if p is not None:
                existing = self.get_property(p.get_urn())
                existing.take_value(p)
    
    def copy(self):
        pass

    def get_urn(self):
        return self.urn

    def __hash__(self):
        return self.entity_id.get_value()


class World(Entity):
    urn = urn.world_urn

    def __init__(self, entity_id):
        Entity.__init__(self, entity_id)
        self.start_time = p.IntProperty(urn.start_time_urn)
        self.longitude = p.IntProperty(urn.longitude_urn)
        self.latitude = p.IntProperty(urn.latitude_urn)
        self.wind_force = p.IntProperty(urn.wind_force_urn)
        self.wind_direction = p.IntProperty(urn.wind_direction_urn)
        self.register_properties([self.start_time, self.longitude, self.latitude, self.wind_force, self.wind_direction])


class Area(Entity):
    def __init__(self, entity_id):
        Entity.__init__(self, entity_id)
        self.x = p.IntProperty(urn.x_urn)
        self.y = p.IntProperty(urn.y_urn)
        self.edges = p.EdgeListProperty(urn.edges_urn)
        self.blockades = p.EntityIDListProperty(urn.blockades_urn)
        self.register_properties([self.x, self.y, self.edges, self.blockades])
        self.apexes = None

    def get_edges(self):
        return self.edges.get_value()

    def get_apexes(self):
        if self.apexes is None:
            self.apexes = []
            for edge in self.get_edges():
                self.apexes.append(edge.get_start_x())
                self.apexes.append(edge.get_start_y())

        return self.apexes

    def get_location(self, world_model):
        if self.x.is_defined() and self.y.is_defined():
            return self.x.get_value(), self.y.get_value()
        else:
            return None, None


class Building(Area):
    urn = urn.building_urn

    def __init__(self, entity_id):
        Area.__init__(self, entity_id)
        self.floors = p.IntProperty(urn.floors_urn)
        self.ignition = p.IntProperty(urn.ignition_urn)
        self.fieryness = p.IntProperty(urn.fieryness_urn)
        self.brokenness = p.IntProperty(urn.brokenness_urn)
        self.building_code = p.IntProperty(urn.building_code_urn)
        self.attributes = p.IntProperty(urn.building_attributes_urn)
        self.ground_area = p.IntProperty(urn.ground_area_urn)
        self.total_area = p.IntProperty(urn.total_area_urn)
        self.temperature = p.IntProperty(urn.temperature_urn)
        self.importance = p.IntProperty(urn.importance_urn)
        self.register_properties([self.floors, self.ignition, self.fieryness, self.brokenness, self.building_code])
        self.register_properties([self.attributes, self.ground_area, self.total_area, self.temperature, self.importance])

    def is_on_fire(self):
        fieryness_value = self.fieryness.get_value()
        # HEATING:1 BURNING:2 INFERNO:3
        if fieryness_value == 1 or fieryness_value == 2 or fieryness_value == 3:
            return True
        return False

    def brokenness_value(self):
        brokenness_value = self.brokenness.get_value()
        return brokenness_value
    
    def fieryness_value(self):
        fieryness_value = self.fieryness.get_value()
        return fieryness_value
        
class Road(Area):
    urn = urn.road_urn

    def __init__(self, entity_id):
        Area.__init__(self, entity_id)


class Blockade(Entity):
    urn = urn.blockade_urn

    def __init__(self, entity_id):
        Entity.__init__(self, entity_id)
        self.x = p.IntProperty(urn.x_urn)
        self.y = p.IntProperty(urn.y_urn)
        self.position = p.EntityIDProperty(urn.position_urn)
        self.apexes = p.IntArrayProperty(urn.apexes_urn)
        self.repair_cost = p.IntProperty(urn.repair_cost_urn)
        self.register_properties([self.x, self.y, self.position, self.apexes, self.repair_cost])

    def get_apexes(self):
        return self.apexes.get_value()

    def get_location(self, world_model):
        if self.x.is_defined() and self.y.is_defined():
            return self.x.get_value(), self.y.get_value()
        else:
            return None, None



class Refuge(Building):
    urn = urn.refuge_urn

    def __init__(self, entity_id):
        Building.__init__(self, entity_id)


class Hydrant(Road):
    urn = urn.hydrant_urn

    def __init__(self, entity_id):
        Road.__init__(self, entity_id)


class GasStation(Building):
    urn = urn.gas_station_urn

    def __init__(self, entity_id):
        Building.__init__(self, entity_id)


class FireStationEntity(Building):
    urn = urn.fire_station_urn

    def __init__(self, entity_id):
        Building.__init__(self, entity_id)


class AmbulanceCentreEntity(Building):
    urn = urn.ambulance_centre_urn

    def __init__(self, entity_id):
        Building.__init__(self, entity_id)


class PoliceOfficeEntity(Building):
    urn = urn.police_office_urn

    def __init__(self, entity_id):
        Building.__init__(self, entity_id)


class Human(Entity):
    def __init__(self, entity_id):
        Entity.__init__(self, entity_id)
        self.x = p.IntProperty(urn.x_urn)
        self.y = p.IntProperty(urn.y_urn)
        self.travel_distance = p.IntProperty(urn.travel_distance_urn)
        self.position = p.EntityIDProperty(urn.position_urn)
        self.position_history = p.IntArrayProperty(urn.position_history_urn)
        self.direction = p.IntProperty(urn.direction_urn)
        self.stamina = p.IntProperty(urn.stamina_urn)
        self.hp = p.IntProperty(urn.hp_urn)
        self.damage = p.IntProperty(urn.damage_urn)
        self.buriedness = p.IntProperty(urn.buriedness_urn)
        self.register_properties([self.x, self.y, self.travel_distance, self.position, self.position_history])
        self.register_properties([self.direction, self.stamina, self.hp, self.damage, self.buriedness])

    def get_position(self):
        return self.position.get_value()

    def get_location(self, world_model):
        if self.x.is_defined() and self.y.is_defined():
            return self.x.get_value(), self.y.get_value()
        if self.position.is_defined():
            pos_entity = world_model.get_entity(self.get_position())
            return pos_entity.get_location(world_model)
        return None, None

    def __str__(self):
        return str(self.position.get_value())


class Civilian(Human):
    urn = urn.civilian_urn

    def __init__(self, entity_id):
        Human.__init__(self, entity_id)


class FireBrigadeEntity(Human):
    urn = urn.fire_brigade_urn

    def __init__(self, entity_id):
        Human.__init__(self, entity_id)
        self.water = p.IntProperty(urn.water_urn)
        self.register_properties([self.water])

    def fire_b_hp(self):
        fire_b_hp = self.hp
        return fire_b_hp

class AmbulanceTeamEntity(Human):
    urn = urn.ambulance_team_urn

    def __init__(self, entity_id):
        Human.__init__(self, entity_id)


class PoliceForceEntity(Human):
    urn = urn.police_force_urn

    def __init__(self, entity_id):
        Human.__init__(self, entity_id)


if __name__ == '__main__':
    id1 = wm.EntityID(10)
    id2 = wm.EntityID(20)
    id3 = wm.EntityID(10)
    id4 = wm.EntityID(10)
    my_dict = {}
    my_dict[id1] = id1
    my_dict[id2] = id2

    print('id1:' + str(id1) + ' id2:' + str(id2) + ' id3:' + str(id3))
    print('id3 from dict:' + str(my_dict[id4]))

    for my_key in my_dict:
        print(str(type(my_key.get_value())))

