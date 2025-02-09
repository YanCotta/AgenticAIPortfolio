import logging
import logging.config
import json
import os

def configure_logging():
    """
    Configures logging using a dictionary-based configuration.
    """
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                'class': 'logging.Formatter',
                'format': '{"time": "%(asctime)s", "level": "%(levelname)s", "agent_name": "%(agent_name)s", "task_id": "%(task_id)s", "message": "%(message)s", "module": "%(module)s", "funcName": "%(funcName)s", "lineno": "%(lineno)d"}'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'json',
                'level': log_level,
                'stream': 'ext://sys.stdout'
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console'],
                'level': log_level,
                'propagate': True
            },
        },
    }
    
    logging.config.dictConfig(logging_config)

class AgentLoggerAdapter(logging.LoggerAdapter):
    """
    Logger adapter to include agent_name and task_id in log messages.
    """
    def __init__(self, logger, extra=None):
        super().__init__(logger, extra or {})

    def process(self, msg, kwargs):
        extra = self.extra.copy()
        if 'extra' in kwargs:
            extra.update(kwargs['extra'])
        kwargs['extra'] = extra
        return msg, kwargs

# Call this function to configure logging
configure_logging()

# Example usage:
# logger = AgentLoggerAdapter(logging.getLogger(__name__), {'agent_name': 'MarketNewsMonitor', 'task_id': '123'})
# logger.info('Starting task', extra={'module': 'market_analysis', 'funcName': 'analyze_news', 'lineno': 42})
