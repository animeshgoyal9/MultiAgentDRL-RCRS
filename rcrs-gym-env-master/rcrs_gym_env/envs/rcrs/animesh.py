from message import AKConnect
from message import KAConnectOK
from message import KAConnectError
from message import AKAcknowledge
from message import KASense
from message import AKExtinguish
from message import AKMove
from urn import *
from world_model import WorldModel
from world_model import Building, EntityID, Edge, Human, Entity, FireBrigadeEntity, World
from rescue_agent import FireBrigadeAgent, RescueAgent
import sys
import util
import random


while True:
	entity_1 = EntityID(210552869)
	entity_1.get_value()
	# print(entity_1)

	entity_2 = EntityID(959)
	# entity_2.get_value()
	# print(entity_2)

	# entity = Entity(entity_1)
	# print(entity.get_properties())

	FireB = FireBrigadeEntity(entity_1)
	print(FireB.hp)
	print(FireB.x)
	print(FireB.y)
	print(FireB.get_position())

	FireBAgent = FireBrigadeAgent()
	print("%%%%" + FireBAgent.position_of_building(entity_2))

	BuildingB = Building(entity_2)
	print(BuildingB.floors)

	print("******************")
