from collections import deque


class InputStream:
    def __init__(self, data_string):
        self.byte_queue = None
        self.set_data_string(data_string)

    def set_data_string(self, data_string):
        self.byte_queue = deque(list(data_string))

    def read(self, count=-1):
        if count == -1:
            return ''.join(self.byte_queue)
        else:
            if len(self.byte_queue) <= count:
                return ''.join(self.byte_queue)
            else:
                data_list = []
                for i in range(count):
                    data_list.append(self.byte_queue.popleft())
                return ''.join(data_list)
        return ''


class OutputStream:
    def __init__(self):
        self.byte_array = []

    def write(self, data_string):
        self.byte_array.extend(list(data_string))

    def getvalue(self):
        return ''.join(self.byte_array)
