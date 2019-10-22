from message_component import IntComp
from message_component import StringComp
from message_component import StringListComp

from message_component import EntityIDComp
from message_component import EntityListComp
from message_component import ConfigComp
from message_component import ChangeSetComp
from message_component import CommandListComp
from message_component import EntityIDListComp
from message_component import IntListComp
from message_component import RawDataComp

msg_urns = {}

def all_msg_urns():
    if len(msg_urns) == 0:
        msg_urns[AKConnect.urn] = 'AKConnect'
        msg_urns[AKAcknowledge.urn] = 'AKAcknowledge'
        msg_urns[KAConnectOK.urn] = 'KAConnectOK'
        msg_urns[KAConnectError.urn] = 'KAConnectError'
        msg_urns[KASense.urn] = 'KASense'
        return msg_urns
    else:
        return msg_urns


class Message:
    def __init__(self):
        self.components = []

    def add_component(self, comp):
        self.components.append(comp)

    def write(self, output_stream):
        for comp in self.components:
            comp.write(output_stream)

    def read(self, input_stream):
        for comp in self.components:
            comp.read(input_stream)


class AKConnect(Message):
    urn = 'urn:rescuecore2:messages.control:ak_connect'

    def __init__(self):
        Message.__init__(self)
        self.request_id_comp = IntComp()
        self.version_comp = IntComp()
        self.agent_name_comp = StringComp()
        self.requested_entities_comp = StringListComp()

        self.add_component(self.request_id_comp)
        self.add_component(self.version_comp)
        self.add_component(self.agent_name_comp)
        self.add_component(self.requested_entities_comp)

    def set_message(self, request_id, version, agent_name, requested_entity_types):
        self.request_id_comp.set_value(request_id)
        self.version_comp.set_value(version)
        self.agent_name_comp.set_value(agent_name)
        self.requested_entities_comp.set_value(requested_entity_types)


class AKAcknowledge(Message):
    urn = 'urn:rescuecore2:messages.control:ak_acknowledge'

    def __init__(self, request_id, agent_id):
        Message.__init__(self)
        self.request_id_comp = IntComp()
        self.agent_id_comp = EntityIDComp()

        self.add_component(self.request_id_comp)
        self.add_component(self.agent_id_comp)

        self.set_message(request_id, agent_id)

    def set_message(self, request_id, agent_id):
        self.request_id_comp.set_value(request_id)
        self.agent_id_comp.set_value(agent_id)


class KAConnectOK(Message):
    urn = 'urn:rescuecore2:messages.control:ka_connect_ok'

    def __init__(self):
        Message.__init__(self)
        self.request_id_comp = IntComp()
        self.agent_id_comp = EntityIDComp()
        self.world_comp = EntityListComp()
        self.config_comp = ConfigComp()

        self.add_component(self.request_id_comp)
        self.add_component(self.agent_id_comp)
        self.add_component(self.world_comp)
        self.add_component(self.config_comp)

    def set_message(self, request_id, agent_id, entities, config):
        self.request_id_comp.set_value(request_id)
        self.agent_id_comp.set_value(agent_id)
        self.world_comp.set_entities(entities)
        self.config_comp.set_config(config)


class KAConnectError(Message):
    urn = 'urn:rescuecore2:messages.control:ka_connect_error'

    def __init__(self):
        Message.__init__(self)
        self.request_id_comp = IntComp()
        self.reason_comp = StringComp()

        self.add_component(self.request_id_comp)
        self.add_component(self.reason_comp)

    def set_message(self, request_id, reason):
        self.request_id_comp.set_value(request_id)
        self.reason_comp.set_value(reason)


class KASense(Message):
    urn = 'urn:rescuecore2:messages.control:ka_sense'

    def __init__(self):
        Message.__init__(self)
        self.agent_id = EntityIDComp()
        self.time = IntComp()
        self.updates = ChangeSetComp()
        self.hear = CommandListComp()

        self.add_component(self.agent_id)
        self.add_component(self.time)
        self.add_component(self.updates)
        self.add_component(self.hear)

    def get_change_set(self):
        return self.updates.get_change_set()

    def get_hearing(self):
        return self.hear.get_commands()

    def get_time(self):
        return self.time.get_value()


# command messages send by agents to the kernel
class Command(Message):
    def __init__(self):
        Message.__init__(self)
        self.agent_id = EntityIDComp()
        self.time = IntComp()
        self.add_component(self.agent_id)
        self.add_component(self.time)


class AKMove(Command):
    urn = 'urn:rescuecore2.standard:message:move'

    def __init__(self):
        Command.__init__(self)
        self.path = EntityIDListComp()
        self.x = IntComp()
        self.y = IntComp()
        self.add_component(self.path)
        self.add_component(self.x)
        self.add_component(self.y)
        self.x.set_value(-1)
        self.y.set_value(-1)


class AKRest(Command):
    urn = 'urn:rescuecore2.standard:message:rest'

    def __init__(self):
        Command.__init__(self)


class AKExtinguish(Command):
    urn = 'urn:rescuecore2.standard:message:extinguish'

    def __init__(self):
        Command.__init__(self)
        self.target = EntityIDComp()
        self.water = IntComp()
        self.add_component(self.target)
        self.add_component(self.water)


class AKClear(Command):
    urn = 'urn:rescuecore2.standard:message:clear'

    def __init__(self):
        Command.__init__(self)
        self.target = EntityIDComp()
        self.add_component(self.target)


class AKClearArea(Command):
    urn = 'urn:rescuecore2.standard:message:clear_area'

    def __init__(self):
        Command.__init__(self)
        self.x = IntComp()
        self.y = IntComp()
        self.add_component(self.x)
        self.add_component(self.y)


class AKRescue(Command):
    urn = 'urn:rescuecore2.standard:message:rescue'

    def __init__(self):
        Command.__init__(self)
        self.target = EntityIDComp()
        self.add_component(self.target)


class AKLoad(Command):
    urn = 'urn:rescuecore2.standard:message:load'

    def __init__(self):
        Command.__init__(self)
        self.target = EntityIDComp()
        self.add_component(self.target)


class AKUnload(Command):
    urn = 'urn:rescuecore2.standard:message:unload'

    def __init__(self):
        Command.__init__(self)

class AKSubscribe(Command):
    urn = 'urn:rescuecore2.standard:message:subscribe'

    def __init__(self):
        Command.__init__(self)
        self.channels = IntListComp()
        self.add_component(self.channels)


class AKSay(Command):
    urn = 'urn:rescuecore2.standard:message:say'

    def __init__(self):
        Command.__init__(self)
        self.data = RawDataComp()
        self.add_component(self.data)


class AKSpeak(Command):
    urn = 'urn:rescuecore2.standard:message:speak'

    def __init__(self):
        Command.__init__(self)
        self.channel = IntComp()
        self.data = RawDataComp()
        self.add_component(self.channel)
        self.add_component(self.data)