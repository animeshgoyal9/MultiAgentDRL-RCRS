import world_model as wm


def create_entity(entity_id, urn):
    if urn == wm.Building.urn:
        return wm.Building(entity_id)
    elif urn == wm.Road.urn:
        return wm.Road(entity_id)
    elif urn == wm.World.urn:
        return wm.World(entity_id)
    elif urn == wm.Blockade.urn:
        return wm.Blockade(entity_id)
    elif urn == wm.Refuge.urn:
        return wm.Refuge(entity_id)
    elif urn == wm.Hydrant.urn:
        return wm.Hydrant(entity_id)
    elif urn == wm.GasStation.urn:
        return wm.GasStation(entity_id)
    elif urn == wm.FireStationEntity.urn:
        return wm.FireStationEntity(entity_id)
    elif urn == wm.AmbulanceCentreEntity.urn:
        return wm.AmbulanceCentreEntity(entity_id)
    elif urn == wm.PoliceOfficeEntity.urn:
        return wm.PoliceOfficeEntity(entity_id)
    elif urn == wm.Civilian.urn:
        return wm.Civilian(entity_id)
    elif urn == wm.FireBrigadeEntity.urn:
        return wm.FireBrigadeEntity(entity_id)
    elif urn == wm.AmbulanceTeamEntity.urn:
        return wm.AmbulanceTeamEntity(entity_id)
    elif urn == wm.PoliceForceEntity.urn:
        return wm.PoliceForceEntity(entity_id)
    else:
        print('unknown entity urn:' + urn)
        return None
