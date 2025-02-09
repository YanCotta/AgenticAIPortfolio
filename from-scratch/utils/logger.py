import logging
import logging.handlers
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        # Include request tracing if available
        if hasattr(record, "request_id"):
            log_record["request_id"] = record.request_id
        return json.dumps(log_record)

def setup_logger(name, log_file="app.log", level=logging.INFO,
                 max_bytes=10 * 1024 * 1024, backup_count=5,
                 shipping_enabled=False, shipping_endpoint=None):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        # Log rotation
        rotating_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        formatter = JsonFormatter('%Y-%m-%d %H:%M:%S')
        rotating_handler.setFormatter(formatter)
        logger.addHandler(rotating_handler)

        # StreamHandler for console output
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    
    # Log filtering: filter out messages below the configured level
    class LevelFilter(logging.Filter):
        def filter(self, record):
            return record.levelno >= level
    logger.addFilter(LevelFilter())

    # Custom handler for log shipping if enabled
    if shipping_enabled and shipping_endpoint:
        class LogShippingHandler(logging.Handler):
            def emit(self, record):
                log_entry = self.format(record)
                # In production, send this log_entry to the shipping_endpoint via HTTP requests
                print(f"Shipping log to {shipping_endpoint}: {log_entry}")
        shipping_handler = LogShippingHandler()
        shipping_handler.setFormatter(formatter)
        logger.addHandler(shipping_handler)

    return logger

# Global logger instance setup with log shipping enabled as an example
logger = setup_logger("app_logger", shipping_enabled=True, shipping_endpoint="http://logserver.example.com/ingest")

# Performance logging helper
def log_performance(metric_name, value, request_id=None):
    extra = {"request_id": request_id} if request_id else {}
    logger.info(f"Performance: {metric_name} = {value}", extra=extra)

# Request tracing: Filter to attach a request_id to log records
class RequestIdFilter(logging.Filter):
    def __init__(self, request_id):
        super().__init__()
        self.request_id = request_id
    def filter(self, record):
        record.request_id = self.request_id
        return True

def add_request_tracing(logger_instance, request_id):
    logger_instance.addFilter(RequestIdFilter(request_id))
