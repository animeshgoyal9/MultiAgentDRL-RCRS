from __future__ import print_function
import logging
import time

import grpc

import AgentInfo_pb2
import AgentInfo_pb2_grpc
import BuildingInfo_pb2
import BuildingInfo_pb2_grpc


def run_adf(bid):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:9090') as channel:
        stub = AgentInfo_pb2_grpc.AnimFireChalAgentStub(channel)
        response = stub.getAgentInfo(AgentInfo_pb2.ActionInfo(actions = [
        	AgentInfo_pb2.Action(agent_id = 210552869, building_id=bid), AgentInfo_pb2.Action(agent_id = 2, building_id=2)]))
    print(response.agents)

def run_reward():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:2212') as channel:
        stub = BuildingInfo_pb2_grpc.AnimFireChalBuildingStub(channel)
        # response = stub.getBuildingInfo(BuildingInfo_pb2.BuildingInfo(buildings = [
        	# BuildingInfo_pb2.Building(fieryness = 1, temperature=1, building_id = 1), BuildingInfo_pb2.Building(fieryness = 2, temperature=2, building_id = 2)]))
        response_reward = stub.getRewards(BuildingInfo_pb2.Empty())
    print(response_reward.reward)

def run_server():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:4007') as channel:
        stub = BuildingInfo_pb2_grpc.AnimFireChalBuildingStub(channel)
        # response = stub.getBuildingInfo(BuildingInfo_pb2.BuildingInfo(buildings = [
            # BuildingInfo_pb2.Building(fieryness = 1, temperature=1, building_id = 1), BuildingInfo_pb2.Building(fieryness = 2, temperature=2, building_id = 2)]))
        response = stub.getBuildingInfo(BuildingInfo_pb2.Empty())
    for i in response.buildings:
        print(i.fieryness, " ", i.temperature, " ", i.building_id)
    print("*******************************************")

if __name__ == '__main__':
    logging.basicConfig()
    while True:
        run_adf(249)
        run_reward()
        run_server()
        time.sleep(10)
        run_adf(298)
        run_reward()
        run_server()
        time.sleep(10)
        run_adf(250)
        run_reward()
        run_server()
        time.sleep(10)
        run_adf(254)
        run_reward()
        run_server()
        time.sleep(10)


