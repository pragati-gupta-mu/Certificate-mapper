"""
Example usage of Azure AI Studio configuration in your application.
This shows how to use the environment variables from config.py
"""

from config import get_config, validate_environment


def initialize_azure_client():
    """Initialize Azure AI client using environment configuration."""
    try:
        # Validate that all required environment variables are present
        validate_environment()
        
        # Get configuration
        config = get_config()
        azure_config = config['azure']
        
        print("🔧 Initializing Azure AI Studio client...")
        print(f"📍 Endpoint: {azure_config['project_endpoint']}")
        print(f"🤖 Model: {azure_config['model_deployment']}")
        
        # Here you would typically initialize your Azure AI client
        # For example, if using Azure AI Projects:
        """
        from azure.ai.projects import AIProjectClient
        from azure.identity import DefaultAzureCredential
        
        client = AIProjectClient(
            endpoint=azure_config['project_endpoint'],
            credential=DefaultAzureCredential(),
            subscription_key=azure_config['subscription_key']
        )
        """
        
        return {
            'endpoint': azure_config['project_endpoint'],
            'model': azure_config['model_deployment'],
            'subscription_key': azure_config['subscription_key'],
            'bing_connection': azure_config['bing_connection_name']
        }
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        return None


def example_streamlit_usage():
    """Example of how to use this in your Streamlit app."""
    
    # At the top of your streamlit_ui.py, you would do:
    """
    import streamlit as st
    from config import get_config, validate_environment
    
    # Initialize configuration
    try:
        validate_environment()
        config = get_config()
        azure_config = config['azure']
        
        # Use the configuration
        st.title("Certificate Mapper")
        st.write(f"Using model: {azure_config['model_deployment']}")
        
        # Initialize your Azure client here
        # client = initialize_azure_client()
        
    except ValueError as e:
        st.error(f"Configuration Error: {e}")
        st.stop()
    """
    pass


if __name__ == "__main__":
    # Test the configuration
    client_config = initialize_azure_client()
    
    if client_config:
        print("✅ Azure configuration loaded successfully!")
        print("🚀 Your app is ready to use Azure AI Studio")
    else:
        print("❌ Failed to load Azure configuration")
        print("💡 Make sure your .env file has all required variables")