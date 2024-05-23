import logging
from fastapi import Request


def setup_logging(log_file):
    """
    Set up the logging configuration.
    Args:
        log_file (str): The name of the file to which logs will be written.
    """
    logging.basicConfig(
        filename=log_file,  # Name of the log file
        level=logging.INFO,  # Log level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
        datefmt='%Y-%m-%d %H:%M:%S'  # Date format in logs
    )
    # Set the logger for your specific application modules
    app_logger = logging.getLogger('app')
    app_logger.setLevel(logging.INFO)


async def log_requests(request: Request, call_next):
    """
    Middleware function to log incoming requests and outgoing responses.
    Args:
        request (Request): The incoming HTTP request.
        call_next (function): The next middleware or request handler.
    Returns:
        Response: The outgoing HTTP response.
    """
    logger = logging.getLogger('app')
    client_ip = request.client.host
    logger.info(f"Request from {client_ip}: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status code: {response.status_code}")
    return response
