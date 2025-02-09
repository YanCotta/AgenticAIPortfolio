import abc
import time
import logging
import asyncio
from utils.logger import setup_logger

class BaseAgent(abc.ABC):
    def __init__(self, name):
        self.name = name
        self.logger = setup_logger(name)
        self._state = {}  # state management
        self.metrics = {"total_duration": 0, "num_tasks": 0}  # performance metrics

    # State getter/setter
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

    # Input/Output Validation Methods
    def validate_input(self, data):
        # Raise ValueError for invalid input if necessary
        return True

    def validate_output(self, result):
        # Raise ValueError for invalid output if necessary
        return True

    # Error classification system
    def _classify_error(self, exc):
        if isinstance(exc, TimeoutError):
            return "TimeoutError"
        elif isinstance(exc, ValueError):
            return "ValidationError"
        else:
            return "GenericError"

    # Synchronous retry mechanism with exponential backoff
    def _retry(self, func, *args, retries=3, backoff=1, **kwargs):
        attempt = 0
        while attempt < retries:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Attempt {attempt+1} failed with error: {self._classify_error(e)}")
                time.sleep(backoff * (2 ** attempt))
                attempt += 1
        self.logger.error("All retry attempts failed.")
        return None

    # Asynchronous retry mechanism with exponential backoff
    async def _retry_async(self, coro, *args, retries=3, backoff=1, **kwargs):
        attempt = 0
        while attempt < retries:
            try:
                return await coro(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Attempt {attempt+1} failed with error: {self._classify_error(e)}")
                await asyncio.sleep(backoff * (2 ** attempt))
                attempt += 1
        self.logger.error("All async retry attempts failed.")
        return None

    @abc.abstractmethod
    def process(self, data):
        """Processes input data and returns results."""
        pass

    # Async version of process
    async def aprocess(self, data):
        """Asynchronously processes input data and returns results."""
        return await asyncio.get_event_loop().run_in_executor(None, self.process, data)

    # Modified synchronous execute with input validation, retry, metrics, and output validation
    def execute(self, data, timeout=10, retries=3, backoff=1):
        self.validate_input(data)
        start_time = time.time()
        result = self._retry(self.process, data, retries=retries, backoff=backoff)
        duration = time.time() - start_time
        self.metrics["total_duration"] += duration
        self.metrics["num_tasks"] += 1
        try:
            self.validate_output(result)
        except Exception as e:
            self.logger.error(f"Output validation failed: {self._classify_error(e)}")
        self.logger.info(f"{self.name} completed task in {duration:.2f} sec")
        return result

    # Async execute using the async retry mechanism
    async def aexecute(self, data, timeout=10, retries=3, backoff=1):
        self.validate_input(data)
        start_time = time.time()
        result = await self._retry_async(self.aprocess, data, retries=retries, backoff=backoff)
        duration = time.time() - start_time
        self.metrics["total_duration"] += duration
        self.metrics["num_tasks"] += 1
        try:
            self.validate_output(result)
        except Exception as e:
            self.logger.error(f"Output validation failed: {self._classify_error(e)}")
        self.logger.info(f"{self.name} completed async task in {duration:.2f} sec")
        return result
