import logging
import logging.handlers
import os

# Create logs directory if not exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Log file settings
log_file = 'logs/app.log'
max_log_size = 1024 * 1024 * 5  # 5 MB
backup_count = 3

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(req_id)s] %(message)s',
    handlers=[
        logging.handlers.RotatingFileHandler(
            log_file, maxBytes=max_log_size, backupCount=backup_count, encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)

class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.req_id = getattr(record, 'req_id', 'no-id')
        return True

logging.getLogger().addFilter(RequestIDFilter())


def generate_request_id():
    import uuid
    return str(uuid.uuid4())
