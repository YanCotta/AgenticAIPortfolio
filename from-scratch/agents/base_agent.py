import abc
import time
import logging
from utils.logger import setup_logger

class BaseAgent(abc.ABC):
    def __init__(self, name):
        self.name = name
        self.logger = setup_logger(name)

    @abc.abstractmethod
    def process(self, data):
        """Processes input data and returns results."""
        pass

    def execute(self, data, timeout=10):
        """Executes the process method with a timeout."""
        start_time = time.time()
        try:
            result = self.process(data)
            duration = time.time() - start_time
            self.logger.info(f"{self.name} completed task in {duration:.2f} sec")
            return result
        except Exception as e:
            self.logger.error(f"{self.name} failed: {str(e)}")
            return None
