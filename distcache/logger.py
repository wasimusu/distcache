from collections import deque
import pickle


class Logger:
    """
    Implements a simple logger
    """

    def __init__(self, filename='cache.db', mode='ab', batch_size=1):
        """
        Initializes Logger object:

        :param filename: name of the file in which logs are to be stored/written.
        :param batch_size: Number of logs to accumulate before log is written.
        To write objects in batches, increase the value of batch_size.
        """
        self.filename = filename
        self.mode = mode
        self.batch_size = batch_size
        self.logs = deque()  # List of logs to be written to the file
        self.file = open(file=filename, mode=mode)

    def log_bytes(self, object):
        """
        Write objects of bytes type in batches to the log file
        :param object: basically any serialized object

        for instance:
            obj = ("life", "is wonderful")
            byte_obj = pickle.dumps(obj)
            logger = Logger()
            logger.log_bytes(byte_obj)

        You can do the same with images or pdfs
            obj = open("some_image_file.png", mode='rb').read()
            logger = Logger()
            logger.log_bytes(byte_obj)

        Note: This function does not check if the object is not bytes. The user should do the checks.

        :returns: None
        """
        self.logs.append(object)
        if len(self.logs) == self.batch_size:
            self.flush()  # TODO: Gotta be async

    def log(self, object):
        """
        Write objects that are not bytes type in batches to the log file
        :param object: basically anything [int, str, list, etc]

        Object instances:
            ("set", "hi", "greeting"),
            ("set", 1, 100),
            ("del", 1)

        :returns: None
        """
        self.logs.append(pickle.dumps(object))
        if len(self.logs) == self.batch_size:
            self.flush()  # TODO: Gotta be async

    def flush(self):
        """
        Writes whatever object is in the log queue is written to the disk.
        No worries if someone appended to the logs when it is being written
        """
        n = len(self.logs)
        for i in range(n):
            pickle.dump(self.logs.popleft(), self.file)

    def close(self):
        """
        Close the logger. Close the log file safely
        """
        self.flush()
        self.file.close()

    def read_logs(self):
        """
        Reads logs from the file.
        """
        self.file.close()
        objs = []
        with open(self.filename, mode='rb') as file:
            while True:
                try:
                    obj = pickle.load(file)
                    objs.append(obj)
                except EOFError as e:
                    break

        self.file = open(self.filename, mode='ab')  # Open the file again but in an append mode of-course.
        return objs
