import logging
import uuid
import os
import glob

def get_file_size(file_path):
    return os.path.getsize(file_path)

def find_latest_log_file(directory, file_extension='*.log'):
    search_pattern = os.path.join(directory, file_extension)
    log_files = glob.glob(search_pattern)
    if not log_files:
        print("No log files found in the directory.")
        return None
    latest_log_file = max(log_files, key=os.path.getctime)
    size = os.path.getsize(latest_log_file)
    print(f"The most recently created log file is: {latest_log_file}")
    return latest_log_file

def logfile_to_send():
    logs_directory = 'logs'
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    last_log = find_latest_log_file(logs_directory)
    if last_log is not None:
        last_log_size = get_file_size(last_log)
        log_number = ''.join([i for i in last_log if i.isdigit()])
        if log_number:
            number = int(log_number)
        else:
            number = 0
        if last_log_size >= 20000:
            number += 1
    else:
        number = 0

    next_log_file = f"log{number}.log"
    log_file = os.path.join(logs_directory, next_log_file)
    return log_file

file_name = logfile_to_send()
logging.basicConfig(level=logging.INFO, filename=file_name,
                    format='%(asctime)s - %(name)s - %(levelname)s - [%(req_id)s] - %(message)s')

logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('aiohttp').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.WARNING)

class HTTPRequestFilter(logging.Filter):
    def filter(self, record):
        return 'HTTP Request' not in record.getMessage()

logging.getLogger().addFilter(HTTPRequestFilter())

def generate_request_id():
    return str(uuid.uuid4())
