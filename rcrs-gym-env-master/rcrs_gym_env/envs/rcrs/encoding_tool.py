from data_stream import OutputStream, InputStream
import message_factory
import entity_factory
import property_factory
import world_model as wm


def write_int32(value, output_stream):
    output_stream.write(chr((value >> 24) & 0xFF))
    output_stream.write(chr((value >> 16) & 0xFF))
    output_stream.write(chr((value >> 8) & 0xFF))
    output_stream.write(chr(value & 0xFF))


def read_int32_from_byte_arr(byte_array):
    value = int((ord(byte_array[0]) << 24) + (ord(byte_array[1]) << 16) + (ord(byte_array[2]) << 8) + ord(byte_array[3]))
    return value


def read_int32(input_stream):
    byte_array = input_stream.read(4)
    return read_int32_from_byte_arr(byte_array)


# def write_double(value, output_stream):
#     packed = struct.pack('!d', value)
#     output_stream.write(packed)


# def read_double(input_stream):
#     byte_array = input_stream.read(8)
#     return struct.unpack('!d', byte_array)


def write_str(value, output_stream):
    write_int32(len(value), output_stream)
    output_stream.write(value)


def read_str(input_stream):
    str_len = read_int32(input_stream)
    return input_stream.read(str_len)


def write_msg(msg, output_stream):
    tmp_output_stream = OutputStream()
    msg.write(tmp_output_stream)
    msg_data = tmp_output_stream.getvalue()

    write_str(msg.urn, output_stream)
    write_int32(len(msg_data), output_stream)
    output_stream.write(msg_data)


def read_msg(input_stream):
    urn = read_str(input_stream)
    data_size = read_int32(input_stream)
    if data_size > 0:
        msg_data = input_stream.read(data_size)
        msg = message_factory.create_msg(urn, msg_data)
        return msg

    return None
        

def read_boolean(input_stream):
    boolean_char = input_stream.read(1)
    b = ord(boolean_char)
    # print('reading boolean char:' + boolean_char + ' ordvalue:' + str(b))
    return b == 1


def write_boolean(b, output_stream):
    if b:
        output_stream.write(chr(1))
    else:
        output_stream.write(chr(0))


def read_property(input_stream):
    result = None
    urn = read_str(input_stream)
    if urn == "" or urn is None:
        return None
    defined = read_boolean(input_stream)
    if defined:
        size = read_int32(input_stream)
        property_byte_array = input_stream.read(size)
        result = property_factory.create_property(urn, property_byte_array)
        result.set_defined(True)
        # print('read the property')
    return result
        

def write_property(p, output_stream):
    write_str(p.get_urn(), output_stream)
    write_boolean(p.is_defined(), output_stream)
    if p.is_defined():
        tmp_output = OutputStream()
        p.write(tmp_output)
        write_int32(len(tmp_output.getvalue()), output_stream)
        output_stream.write(tmp_output.getvalue())


def read_entity(input_stream):
    urn = read_str(input_stream)
    if urn == "" or urn is None:
        return None
    eid = wm.EntityID(read_int32(input_stream))
    entity_size = read_int32(input_stream)
    entity = entity_factory.create_entity(eid, urn)
    entity.read(input_stream)
    return entity


def write_entity(e, output_stream):
    tmp_output_stream = OutputStream()
    e.write(tmp_output_stream)
    write_str(e.get_urn(), output_stream)
    write_int32(e.get_id().get_value(), output_stream)
    write_int32(len(tmp_output_stream.getvalue()), output_stream)
    output_stream.write(tmp_output_stream.getvalue())


def read_float32(input_stream):
    byte_array = input_stream.read(4)
    return read_float32_from_byte_arr(byte_array)


def read_float32_from_byte_arr(byte_array):
    value = float((ord(byte_array[0]) << 24) + (ord(byte_array[1]) << 18) + (ord(byte_array[2]) << 8) + ord(byte_array[3]))
    return value


def write_float32(value,output_stream):
    output_stream.write(chr((value >> 24) & 0xFF))
    output_stream.write(chr((value >> 16) & 0xFF))
    output_stream.write(chr((value >> 8) & 0xFF))
    output_stream.write(chr(value & 0xFF))
    return


if __name__ == '__main__':
    print("writing the value:549139337")
    output_stream = OutputStream()
    write_int32(549139337, output_stream)
    four_bytes = output_stream.getvalue()
    for my_ch in four_bytes:
        print(ord(my_ch))

    print("reading back")
    input_stream = InputStream(four_bytes)
    read_four_bytes = input_stream.read(4)
    for read_ch in read_four_bytes:
        print(ord(read_ch))

    print("read value:" + str(read_int32_from_byte_arr(read_four_bytes)))
