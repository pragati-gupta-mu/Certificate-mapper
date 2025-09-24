import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Access environment variables
API_KEY = os.getenv('API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'info')

# Streamlit configuration
STREAMLIT_PORT = int(os.getenv('STREAMLIT_SERVER_PORT', 8501))
STREAMLIT_ADDRESS = os.getenv('STREAMLIT_SERVER_ADDRESS', '0.0.0.0')


# Example usage
def get_config():
    """Return application configuration from environment variables."""
    config = {
        'api_key': API_KEY,
        'database_url': DATABASE_URL,
        'debug': DEBUG,
        'log_level': LOG_LEVEL,
        'streamlit': {
            'port': STREAMLIT_PORT,
            'address': STREAMLIT_ADDRESS
        }
    }
    return config


# Validate required environment variables
def validate_environment():
    """Validate that required environment variables are set."""
    required_vars = ['API_KEY']  # Add your required variables here
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        error_msg = (f"Missing required environment variables: "
                     f"{', '.join(missing_vars)}")
        raise ValueError(error_msg)
    
    return True