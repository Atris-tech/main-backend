import logging
from logstash_async.handler import AsynchronousLogstashHandler
import time
host = 'localhost'
port = 5000
# Get you a test logger
test_logger = logging.getLogger('python-logstash-logger')
# Set it to whatever level you want - default will be info
test_logger.setLevel(logging.DEBUG)
# Create a handler for it
async_handler = AsynchronousLogstashHandler(host, port, database_path=None)
# Add the handler to the logger
test_logger.addHandler(async_handler)

if __name__ == '__main__':
    while True:
        test_logger.info("This is an info message at %s", time.time())
        time.sleep(0.5)