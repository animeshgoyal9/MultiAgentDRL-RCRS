import socket
import threading
from encoding_tool import read_int32_from_byte_arr
from encoding_tool import write_int32
from encoding_tool import read_msg
from encoding_tool import write_msg
from data_stream import OutputStream
from data_stream import InputStream
import util

class TCPConnection:
    """The TCP/IP implementation connection"""

    def __init__(self):
        self.socket = None
        self.agent = None
        self.buffer_size = 4096
        self.data_buffer = ''

    def connect(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.socket.settimeout(10) # 10 seconds to wait for connection
        try:
            self.socket.connect((address, port))
        except socket.error, exception:
            # return without creating tcp reading loop
            print(str(exception))
            self.socket.close()
            return

        read_thread = threading.Thread(target=self.read_loop)
        read_thread.daemon = True
        read_thread.start()

    def set_agent(self, _agent):
        self.agent = _agent

    def msg_bytes_received(self, byte_array):
        input_stream = InputStream(byte_array)
        msg = read_msg(input_stream)
        if msg is not None:
            self.agent.message_received(msg)

    def read_loop(self):
        while True:
            try:
                # note that this is blocking call
                message_data = self.recv_msg()
                #print('msg data:' + data_array)
                #util.print_bytes(data_array)
                self.msg_bytes_received(message_data)
            except IOError:
                self.socket.close()
                break

    def recv_msg(self):
        buffer_size = 4096
        msg_size_data = self.data_buffer
        while len(msg_size_data) < 4:
            try:
                msg_size_data += self.socket.recv(buffer_size)
            except socket.error as error_msg:
                raise IOError('tcp client IOError:' + error_msg)

        if msg_size_data:
            msg_size = read_int32_from_byte_arr(msg_size_data[0:4])
            #print('msg.size:' + str(msg_size))
            msg_data = msg_size_data[4:]
            while len(msg_data) < msg_size:
                try:
                    msg_data += self.socket.recv(buffer_size)
                except socket.error as error_msg:
                    raise IOError('tcp client IOError:' + error_msg)
            if msg_data:
                self.data_buffer = msg_data[msg_size:]
                return msg_data[:msg_size]
        else:
            raise IOError('tcp client is disconnected')

        return ''

    def send_msg(self, msg):
        tmp_output_stream = OutputStream()
        write_msg(msg, tmp_output_stream)
        write_int32(0, tmp_output_stream)
        msg_data = tmp_output_stream.getvalue()
        output_stream = OutputStream()
        # first write the size of the message
        write_int32(len(msg_data), output_stream)
        output_stream.write(msg_data)
        self.send_bytes(output_stream.getvalue())

    def send_bytes(self, byte_array):
        self.socket.sendall(byte_array)

    def shutdown(self):
        self.socket.close()
