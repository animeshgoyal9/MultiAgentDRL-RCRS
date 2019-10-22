import message
from data_stream import InputStream

def create_msg(urn, byte_array):
    urns = message.all_msg_urns()
    if urn in urns:
        class_name = urns[urn]
        module_ = __import__('message')
        class_ = getattr(module_, class_name)
        msg_instance = class_()
        msg_instance.read(InputStream(byte_array))
        return msg_instance
    else:
        return None
