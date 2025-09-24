#!/usr/bin/env python3
"""
Environment Variable Demo
Run this to see how your app detects and uses different environments.
"""

from config import get_config, validate_environment, print_environment_info

def main():
    """Demonstrate environment variable usage across different environments."""
    
    print("=" * 60)
    print("🔧 Certificate Mapper - Environment Configuration Demo")
    print("=" * 60)
    
    # Show environment detection
    print_environment_info()
    print()
    
    # Try to load configuration
    try:
        print("📋 Loading configuration...")
        config = get_config()
        
        # Show what's loaded (safely, without exposing secrets)
        print(f"✅ Environment: {config['environment']}")
        print(f"✅ Debug mode: {config['debug']}")
        print(f"✅ Log level: {config['log_level']}")
        print(f"✅ Streamlit port: {config['streamlit']['port']}")
        
        # Show Azure configuration (safely, without exposing full keys)
        azure_config = config['azure']
        if azure_config['project_endpoint']:
            print(f"✅ Azure Project Endpoint: {azure_config['project_endpoint'][:50]}...")
        else:
            print("⚠️  Azure Project Endpoint not found")
            
        if azure_config['model_deployment']:
            print(f"✅ Model Deployment: {azure_config['model_deployment']}")
        else:
            print("⚠️  Model Deployment not found")
            
        if azure_config['subscription_key']:
            key_preview = azure_config['subscription_key'][:8] + "..."
            print(f"✅ Subscription Key: {key_preview}")
        else:
            print("⚠️  Subscription Key not found")
            
        if azure_config['bing_connection_name']:
            conn_preview = azure_config['bing_connection_name'][:60] + "..."
            print(f"✅ Bing Connection: {conn_preview}")
        else:
            print("⚠️  Bing Connection Name not found")
            
        print()
        
        # Validate environment
        print("🔍 Validating required environment variables...")
        validate_environment()
        print("✅ All required environment variables are present!")
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print()
        print("📝 To fix this:")
        
        if config.get('is_local', True):
            print("   1. Create a .env file in the project root")
            print("   2. Copy from .env.example and fill in your values")
            print("   3. Run: cp .env.example .env")
        elif config.get('is_codespaces', False):
            print("   1. Go to GitHub Repository Settings")
            print("   2. Navigate to: Secrets and variables → Codespaces")
            print("   3. Add the missing environment variables")
        else:
            print("   1. Set environment variables in your deployment platform")
            print("   2. Check your hosting provider's documentation")
    
    print("=" * 60)

if __name__ == "__main__":
    main()