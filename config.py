import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development only)
# In production/Codespaces, this will do nothing (no .env file exists)
load_dotenv()

# Detect environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')
IS_LOCAL = ENVIRONMENT == 'local'
IS_CODESPACES = os.getenv('CODESPACES') == 'true'
IS_PRODUCTION = not IS_LOCAL and not IS_CODESPACES

# Azure AI Studio configuration
PROJECT_ENDPOINT = os.getenv('PROJECT_ENDPOINT')
MODEL_DEPLOYMENT = os.getenv('MODEL_DEPLOYMENT')
SUBSCRIPTION_KEY = os.getenv('SUBSCRIPTION_KEY')
BING_CONNECTION_NAME = os.getenv('BING_CONNECTION_NAME')

# Azure Service Principal (for authentication)
AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
AZURE_CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
AZURE_TENANT_ID = os.getenv('AZURE_TENANT_ID')

# Application settings
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'info')

# Streamlit configuration
STREAMLIT_PORT = int(os.getenv('STREAMLIT_SERVER_PORT', 8501))
STREAMLIT_ADDRESS = os.getenv('STREAMLIT_SERVER_ADDRESS', '0.0.0.0')


def get_config():
    """Return application configuration from environment variables."""
    config = {
        'environment': ENVIRONMENT,
        'is_local': IS_LOCAL,
        'is_codespaces': IS_CODESPACES,
        'is_production': IS_PRODUCTION,
        'azure': {
            'project_endpoint': PROJECT_ENDPOINT,
            'model_deployment': MODEL_DEPLOYMENT,
            'subscription_key': SUBSCRIPTION_KEY,
            'bing_connection_name': BING_CONNECTION_NAME,
        },
        'debug': DEBUG,
        'log_level': LOG_LEVEL,
        'streamlit': {
            'port': STREAMLIT_PORT,
            'address': STREAMLIT_ADDRESS
        }
    }
    return config


def validate_environment():
    """Validate that required environment variables are set."""
    required_vars = [
        'PROJECT_ENDPOINT',
        'MODEL_DEPLOYMENT',
        'SUBSCRIPTION_KEY',
        'BING_CONNECTION_NAME'
    ]
    
    # Check if service principal auth is available
    auth_vars = ['AZURE_CLIENT_ID', 'AZURE_CLIENT_SECRET', 'AZURE_TENANT_ID']
    auth_available = all(os.getenv(var) for var in auth_vars)
    
    if not auth_available:
        print("⚠️  Service principal authentication not configured.")
        print("   You may need to set AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID")
    
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        env_info = f" (Environment: {ENVIRONMENT})"
        error_msg = (f"Missing required environment variables: "
                     f"{', '.join(missing_vars)}{env_info}")
        raise ValueError(error_msg)
    
    return True


def print_environment_info():
    """Print current environment information for debugging."""
    print(f"🌍 Environment: {ENVIRONMENT}")
    print(f"📁 Local Development: {IS_LOCAL}")
    print(f"☁️  GitHub Codespaces: {IS_CODESPACES}")
    print(f"🚀 Production: {IS_PRODUCTION}")
    
    if IS_LOCAL:
        print("📝 Using .env file for configuration")
    elif IS_CODESPACES:
        print("🔒 Using GitHub Codespaces secrets")
    else:
        print("⚙️  Using platform environment variables")