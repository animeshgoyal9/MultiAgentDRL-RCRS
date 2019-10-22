from message import AKConnect
from message import KAConnectOK
from message import KAConnectError
from message import AKAcknowledge
from message import KASense
from message import AKExtinguish
from message import AKMove
from urn import *
from world_model import WorldModel
from world_model import Building, EntityID, Edge, Human, FireBrigadeEntity, Entity
import sys
import util
import random


class RescueAgent:
    """The base class for handling the rescue"""

    request_id = 0

    def __init__(self):
        self.connection = None
        self.name = ''
        self.connect_request_id = None
        self.world_model = None
        self.config = None
        self.random = None
        self.entity_id = None
        pass

    def connect(self, _connection):
        self.connection = _connection
        self.connection.set_agent(self)
        connect_msg = AKConnect()
        connect_msg.set_message(RescueAgent.request_id, 1, self.name, self.get_requested_entities())
        self.connect_request_id = RescueAgent.request_id
        RescueAgent.request_id += 1
        self.connection.send_msg(connect_msg)

    def message_received(self, msg):
        if isinstance(msg, KAConnectOK):
            self.handle_connect_ok(msg)
        elif isinstance(msg, KAConnectError):
            self.handle_connect_error(msg)
        elif isinstance(msg, KASense):
            self.process_sense(msg)

    def process_sense(self, msg):
        self.world_model.merge(msg.get_change_set())
        heard = msg.get_hearing()
        self.think(msg.get_time(), msg.get_change_set(), heard)

    def think(self, timestep, change_set, heard):
        print('think method is supposed to be overriden')

    # that will be overriden by agents
    def get_requested_entities(self):
        return ''

    # that will be overriden by agents
    def post_connect(self, agent_id, entities, config):
        self.entity_id = agent_id
        self.world_model = WorldModel()
        self.world_model.add_entities(entities)
        #todo: check whether we need to merge agent config and the config coming from kernel
        self.config = config
        print('post_connect agent_id:' + str(agent_id.get_value()))
        # print('config test comms.channels.count:' + self.config.get_value('comms.channels.count'))

    def handle_connect_ok(self, msg):
        if msg.request_id_comp.get_value() == self.connect_request_id:
            # print("handle connect ok")
            self.post_connect(msg.agent_id_comp.get_value(), msg.world_comp.get_entities(), msg.config_comp.get_config())
            ack_msg = AKAcknowledge(self.connect_request_id, msg.agent_id_comp.get_value())
            self.connection.send_msg(ack_msg)

    def handle_connect_error(self, msg):
        if msg.request_id_comp.get_value() == self.connect_request_id:
            print('KAConnectionError:' + msg.get_reason())

    def random_walk(self, timestep):
        # calculate 10 step path
        path = []
        start_pos = self.get_position()
        print('random walk agent_pos:' + str(start_pos))
        # print(start_pos)
        # construct random path
        for i in range(10):
            edges = self.world_model.get_entity(start_pos).get_edges()
            neighbors = []
            for edge in edges:
                if edge.get_neighbor() is not None:
                    neighbors.append(edge.get_neighbor())
            next = random.choice(neighbors)
            path.append(next)
            start_pos = next

        move_msg = AKMove()
        move_msg.agent_id.set_value(self.entity_id)
        move_msg.time.set_value(timestep)
        move_msg.path.set_ids(path)
        self.send_kernel_msg(move_msg)

    def get_location(self):
        # print("agent_location" + str(self.world_model.get_entity(self.entity_id).get_location(self.world_model)))
        return self.world_model.get_entity(self.entity_id).get_location(self.world_model)

    def get_position(self):
        # print('agent pos:' + str(self.world_model.get_entity(self.entity_id)))
        return self.world_model.get_entity(self.entity_id).get_position()

    def send_kernel_msg(self, msg):
        self.connection.send_msg(msg)


class FireBrigadeAgent(RescueAgent):
    def __init__(self):
        self.name = 'rescue_agent.FireBrigadeAgent'

    def get_requested_entities(self):
        return [fire_brigade_urn]

    def extinguish_the_building(self, building, timestep):
        extinguish_dist = self.config.get_value('fire.extinguish.max-distance')
        building_posx, building_posy = building.get_location(self.world_model)
        agent_posx, agent_posy = self.get_location()
        dist = util.cal_distance(agent_posx, agent_posy, building_posx, building_posy)
        if dist < extinguish_dist:
            ext_msg = AKExtinguish()
            ext_msg.agent_id.set_value(self.entity_id)
            ext_msg.time.set_value(self.timestep)
            ext_msg.target.set_value(building.get_id())
            ext_msg.water.set_value(self.config.get_value('fire.extinguish.max-sum'))
            self.send_kernel_msg(ext_msg)
        else:
            #todo: calculate a path to the building that is on fire
            self.random_walk(timestep)

    def position_of_building(self, building):
        building_posx, building_posy = building.get_location(self.world_model)
        agent_posx, agent_posy = self.get_location()
        print("building x position" + str(building_posx))
        return building_posx

    def think(self, timestep, change_set, heard):
        buildings_on_fire = []
        for entity in self.world_model.get_entities():
            if isinstance(entity, Building):
                if entity.is_on_fire():
                    buildings_on_fire.append(entity)


        agent_posx, agent_posy = self.get_location()
        print("X_position" + str(agent_posx))
        if len(buildings_on_fire) > 0:
            min_dist = sys.maxint
            min_dist_building = None
            for building in buildings_on_fire:
                building_posx, building_posy = building.get_location(self.world_model)
                dist = util.cal_distance(agent_posx, agent_posy, building_posx, building_posy)
                if dist > min_dist:
                    min_dist = dist
                    min_dist_building = building

            # calculate action for the building
            self.extinguish_the_building(min_dist_building, timestep)
        else:
            self.random_walk(timestep)
        print('think finished.')

class AmbulanceTeamAgent(RescueAgent):
    def __init__(self):
        self.name = 'rescue_agent.AmbulanceTeamAgent'

    def get_requested_entities(self):
        return [ambulance_team_urn]

    def think(self, timestep, change_set, heard):
        self.random_walk(timestep)
        print('think finished.')


class PoliceForceAgent(RescueAgent):
    def __init__(self):
        self.name = 'rescue_agent.PoliceForceAgent'

    def get_requested_entities(self):
        return [police_force_urn]

    def think(self, timestep, change_set, heard):
        self.random_walk(timestep)
        print('think finished.')
