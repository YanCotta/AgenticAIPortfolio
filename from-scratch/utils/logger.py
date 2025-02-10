import logging
import logging.handlers
import json
from typing import Optional, Dict, Any
from pathlib import Path
import time
from prometheus_client import Counter, Histogram

# Metrics
log_entries = Counter('log_entries_total', 'Total number of log entries', ['level'])
log_processing_time = Histogram('log_processing_seconds', 'Time spent processing logs')

class JsonFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_msec_format = '%s.%03d'

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON with enhanced metadata"""
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "process_id": record.process,
            "thread_id": record.thread,
        }
        
        # Include exception info if available
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        # Include custom fields
        if hasattr(record, "request_id"):
            log_record["request_id"] = record.request_id
        if hasattr(record, "correlation_id"):
            log_record["correlation_id"] = record.correlation_id
        if hasattr(record, "extra_data"):
            log_record["extra_data"] = record.extra_data

        return json.dumps(log_record)

class MetricsFilter(logging.Filter):
    """Filter to collect metrics about logging"""
    def filter(self, record: logging.LogRecord) -> bool:
        log_entries.labels(level=record.levelname).inc()
        return True

def setup_logger(
    name: str,
    log_file: str = "app.log",
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    log_dir: Optional[str] = None,
    shipping_endpoint: Optional[str] = None,
) -> logging.Logger:
    """Configure logger with enhanced features"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # Ensure log directory exists
        if log_dir:
            Path(log_dir).mkdir(parents=True, exist_ok=True)
            log_file = str(Path(log_dir) / log_file)

        # File handler with rotation
        rotating_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        formatter = JsonFormatter()
        rotating_handler.setFormatter(formatter)
        logger.addHandler(rotating_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Add metrics collection
        logger.addFilter(MetricsFilter())

        # Optional log shipping
        if shipping_endpoint:
            shipping_handler = LogShippingHandler(shipping_endpoint)
            shipping_handler.setFormatter(formatter)
            logger.addHandler(shipping_handler)

    return logger

class LogShippingHandler(logging.Handler):
    """Handler for shipping logs to external service"""
    def __init__(self, endpoint: str):
        super().__init__()
        self.endpoint = endpoint
        self._buffer: list = []
        self._buffer_size = 100
        self._last_ship_time = time.time()
        self._ship_interval = 5  # seconds

    def emit(self, record: logging.LogRecord) -> None:
        """Buffer and ship logs"""
        try:
            with log_processing_time.time():
                log_entry = self.format(record)
                self._buffer.append(log_entry)
                
                # Ship logs if buffer is full or interval has passed
                if (len(self._buffer) >= self._buffer_size or 
                    time.time() - self._last_ship_time > self._ship_interval):
                    self._ship_logs()
        except Exception as e:
            # Fallback to stderr in case of shipping failure
            import sys
            print(f"Failed to ship log: {str(e)}", file=sys.stderr)

    def _ship_logs(self) -> None:
        """Ship buffered logs to endpoint"""
        if not self._buffer:
            return
            
        try:
            # Here you would implement the actual shipping logic
            # For example, using requests or aiohttp to send to endpoint
            print(f"Shipping {len(self._buffer)} logs to {self.endpoint}")
            self._buffer.clear()
            self._last_ship_time = time.time()
        except Exception as e:
            print(f"Log shipping failed: {str(e)}", file=sys.stderr)

# Global logger instance setup with log shipping enabled as an example
logger = setup_logger("app_logger", shipping_endpoint="http://logserver.example.com/ingest")

# Performance logging helper
def log_performance(logger: logging.Logger, metric_name: str, value: float, 
                   request_id: Optional[str] = None, 
                   extra_data: Optional[Dict[str, Any]] = None) -> None:
    """Log performance metrics with context"""
    extra = {
        "metric_name": metric_name,
        "value": value,
        "request_id": request_id,
    }
    if extra_data:
        extra["extra_data"] = extra_data
    logger.info(f"Performance metric: {metric_name} = {value}", extra=extra)

# Request tracing filter
class RequestTraceFilter(logging.Filter):
    """Filter to attach request context to log records"""
    def __init__(self, request_id: str, correlation_id: Optional[str] = None):
        super().__init__()
        self.request_id = request_id
        self.correlation_id = correlation_id

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = self.request_id
        if self.correlation_id:
            record.correlation_id = self.correlation_id
        return True

def add_request_context(logger: logging.Logger, 
                       request_id: str, 
                       correlation_id: Optional[str] = None) -> None:
    """Add request context to logger"""
    logger.addFilter(RequestTraceFilter(request_id, correlation_id))
