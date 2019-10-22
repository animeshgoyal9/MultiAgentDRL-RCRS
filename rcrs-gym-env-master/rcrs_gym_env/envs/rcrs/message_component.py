import encoding_tool as et
import change_set as cs
import world_model as wm
import config as con


class IntComp:
    def __init__(self):
        self.value = None

    def set_value(self, _value):
        self.value = _value

    def get_value(self):
        return self.value

    def write(self, output_stream):
        et.write_int32(self.value, output_stream)

    def read(self, input_stream):
        self.value = et.read_int32(input_stream)
        
    def __str__(self):
        return str(self.name) + " = " + str(self.value)


class StringComp:
    def __init__(self):
        self.value = None

    def set_value(self, _value):
        self.value = _value

    def get_value(self):
        return self.value

    def write(self, output_stream):
        et.write_str(self.value, output_stream)

    def read(self, input_stream):
        self.value = et.read_str(input_stream)

    def __str__(self):
        return str(self.name) + " = " + str(self.value)


class StringListComp:
    def __init__(self):
        self.value_list = None

    def set_value(self, _value_list):
        self.value_list = _value_list

    def get_value(self):
        return self.value_list

    def write(self, output_stream):
        et.write_int32(len(self.value_list), output_stream)
        for value in self.value_list:
            et.write_str(value, output_stream)

    def read(self, input_stream):
        self.value_list = []
        list_len = et.read_int32(input_stream)
        for i in range(list_len):
            self.value_list.append(et.read_str(input_stream))

    def __str__(self):
        return str(self.name) + " = " + str(self.value_list)


class ChangeSetComp:
    def __init__(self, _change_set=None):
        self.changes = cs.ChangeSet(_change_set)
            
    def get_change_set(self):
        return self.changes
    
    def set_change_set(self, new_change_set):
        self.changes = cs.ChangeSet(new_change_set)
    
    def write(self, output_stream):
        self.changes.write(output_stream)
        
    def read(self, input_stream):
        self.changes = cs.ChangeSet()
        self.changes.read(input_stream)
    
    def __str__(self):
        return " = " + str(len(self.changes.get_changed_entities())) + " entities."


class EntityComp:
    entity = None
    
    def __init__(self,n_entity=None):
        if isinstance(n_entity, wm.Entity):
            self.entity = n_entity
        else:
            self.entity = None
        
    def get_entity(self):
        return self.entity
    
    def set_entity(self, e):
        if isinstance(e, wm.Entity):
            self.entity = e
            
    def write(self, output_string):
        et.write_entity(self.entity, output_string)
        
    def read(self, input_string):
        self.entity = et.read_entity(input_string)

    def __str__(self):
        return str(self.name) + " = " + str(self.entity)


class EntityIDComp:
    def __init__(self, value=None):
        self.value = value
        
    def get_value(self):
        return self.value
    
    def set_value(self, eid):
        self.value = eid
    
    def write(self, output_stream):
        et.write_int32(self.value.get_value(),output_stream)
        
    def read(self,input_stream):
        self.value = wm.EntityID(et.read_int32(input_stream))

    def __str__(self):
        return str(self.name) + " = " + str(self.value)


class EntityIDListComp:
    def __init__(self,nids=None):
        if not (nids is None) and isinstance(nids,list):
            self.ids = nids
        else:
            self.ids = []
    
    def get_ids(self):
        return self.ids
    
    def set_ids(self,nids):
        if not (nids is None) and isinstance(nids,list):
            self.ids = nids
        return
    
    def write(self,output_stream):
        et.write_int32(len(self.ids), output_stream)
        for eid in self.ids:
            et.write_int32(eid.get_value(), output_stream)
        return
    
    def read(self,input_stream):
        self.ids = []
        count = et.read_int32(input_stream)
        for i in range(count):
            eid = wm.EntityID(et.read_int32(input_stream))
            self.ids.append(eid)
        return

    def __str__(self):
        return str(self.name) + " = " + str(self.ids)


class EntityListComp:
    def __init__(self,nents=None):
        if nents is not None:
            self.ents = nents
        else:
            self.ents = []
    
    def get_entities(self):
        return self.ents
    
    def set_entities(self,nents):
        if nents is not None:
            self.ents = nents
    
    def write(self, output_stream):
        et.write_int32(len(self.ents), output_stream)
        for ent in self.ents:
            et.write_entity(ent, output_stream)
    
    def read(self,input_stream):
        self.ents = []
        count = et.read_int32(input_stream)
        for i in range(count):
            e = et.read_entity(input_stream)
            self.ents.append(e)
    
    def __str__(self):
        return str(self.name) + " = " + str(len(self.ents)) + " entities."
        
    
class IntListComp:
    def __init__(self,nints=None):
        if not (nints is None) and isinstance(nints,list):
            self.ints = nints
        else:
            self.ints = []
    
    def get_values(self):
        return self.ints
    
    def set_values(self,nints):
        if not (nints is None) and isinstance(nints,list):
            self.ints = nints
        return
    
    def write(self,output_stream):
        et.write_int32(len(self.ints), output_stream)
        for nt in self.ints:
            et.write_int32(nt,output_stream)
        return
    
    def read(self,input_stream):
        self.ints = []
        count = et.read_int32(input_stream)
        for i in range(count):
            e = et.read_int32(input_stream)
            self.ints.append(e)
        return

    def __str__(self):
        return str(self.name) + " = " + str(self.ints)

    
class CommandListComp:
    def __init__(self, _commands=None):
        if _commands is not None:
            self.commands = _commands
        else:
            self.commands = []

    def get_commands(self):
        return self.commands

    def set_commands(self, _commands):
        self.commands = _commands

    def write(self, output_stream):
        et.write_int32(len(self.commands), output_stream)
        for command in self.commands:
            et.write_msg(command, output_stream)

    def read(self,input_stream):
        self.commands = []
        command_count = et.read_int32(input_stream)
        for i in range(command_count):
            command = et.read_msg(input_stream)
            self.commands.append(command)

    def __str__(self):
        return str(len(self.commands)) + " commands."


class FloatListComp:
    def __init__(self, floats=None):
        if not(floats is None) and isinstance(floats,list):
            self.data = floats
        else:
            self.data = []
            
    def get_values(self):
        return self.data
    
    def set_values(self,floats):
        if not(floats is None) and isinstance(floats,list):
            self.data = floats
        return
    
    def write(self,output_stream):
        et.write_int32(len(self.data), output_stream)
        for f in self.data:
            et.write_float32(f,output_stream)
        return
    
    def read(self,input_stream):
        self.data = []
        count = et.read_int32(input_stream)
        for i in range(count):
            f = et.read_float32(input_stream)
            self.data.append(f)
        return
        
    def __str__(self):
        return str(self.name) + " = " + str(self.data)
    
        
class RawDataComp:
    def __init__(self):
        self.byte_data = None
            
    def get_data(self):
        return self.byte_data
    
    def set_data(self, byte_data_):
        self.byte_data = byte_data_
    
    def write(self, output_stream):
        et.write_int32(len(self.byte_data), output_stream)
        output_stream.write(self.byte_data)
    
    def read(self,input_stream):
        data_size = et.read_int32(input_stream)
        self.byte_data = input_stream.read(data_size)


class ConfigComp:
    def __init__(self):
        self.config = None

    def get_config(self):
        return self.config

    def set_config(self, _config):
        self.config = _config

    def write(self, output_stream):
        keys = self.config.get_keys()
        et.write_int32(len(keys), output_stream)
        for key in keys:
            value = self.config.get_value(key)
            et.write_str(key, output_stream)
            et.write_str(value, output_stream)

    def read(self, input_stream):
        key_count = et.read_int32(input_stream)
        self.config = con.Config()
        for i in range(key_count):
            key = et.read_str(input_stream)
            value = et.read_str(input_stream)
            self.config.set_value(key, value)

    def __str__(self):
        return (self.name) + " = " + str(len(self.byte_data)) + " bytes of raw data."
