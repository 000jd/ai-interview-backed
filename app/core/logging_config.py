import logging
import coloredlogs
import sys

def setup_logging():
    """Set up centralized, colored logging for the application."""
    
    # Define custom color styles
    level_styles = {
        'debug': {'color': 'white'},
        'info': {'color': 'green'},
        'warning': {'color': 'yellow'},
        'error': {'color': 'red'},
        'critical': {'color': 'red', 'bold': True},
    }
    
    # Define custom field styles
    field_styles = {
        'asctime': {'color': 'cyan'},
        'hostname': {'color': 'magenta'},
        'levelname': {'color': 'black', 'bold': True},
        'name': {'color': 'blue'},
        'programname': {'color': 'cyan'},
        'username': {'color': 'yellow'},
    }

    coloredlogs.install(
        level='INFO',
        stream=sys.stdout,
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level_styles=level_styles,
        field_styles=field_styles
    )

    # Make uvicorn use the root logger configuration to avoid duplicate logs
    logging.getLogger("uvicorn.access").handlers = []
    logging.getLogger("uvicorn.error").handlers = []
    logging.getLogger("uvicorn.access").propagate = True
    logging.getLogger("uvicorn.error").propagate = True