import json
from collections import deque

class Logger:
    def __init__(self, filename='cache.json', mode='a', batch_size=1):
        """
        :param filename: Output filename
        :param batch_size: To write objects in batches, increase the value of batch_size
        """
        self.filename = filename
        self.batch_size = batch_size
        self.logs = deque()  # List of logs to be written to the file
        self.file = open(file=filename, mode=mode)

    def log(self, object):
        """
        Write objects in batches to the log file
        :param object: basically anything [int, str, list, etc]
        For instance:
            ("set", "hi", "greeting"),
            ("set", 1, 100),
            ("del", 1)
        :return: None
        """
        self.logs.append(object)
        if len(self.logs) == self.batch_size:
            self.flush()  # TODO: Gotta be async

    def flush(self):
        """
        Writes whatever object is in the log queue to the log file
        No worries if someone appended to the logs when it is being written
        """
        n = len(self.logs)
        for i in range(n):
            self.file.write(json.dumps(self.logs.popleft()))
            self.file.write('\n')

    def close(self):
        """
        Close the logger. Close the log file safely
        """
        self.flush()
        self.file.close()
