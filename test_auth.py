#!/usr/bin/env python3
"""
Test Azure Service Principal Authentication
Use this to verify your service principal credentials work before using them in your app.
"""

import os
from azure.identity import ClientSecretCredential
from azure.core.exceptions import ClientAuthenticationError

def test_service_principal():
    """Test if service principal authentication works."""
    
    print("🔐 Testing Azure Service Principal Authentication...")
    print("=" * 60)
    
    # Get credentials from environment or prompt
    client_id = os.getenv('AZURE_CLIENT_ID')
    client_secret = os.getenv('AZURE_CLIENT_SECRET')
    tenant_id = os.getenv('AZURE_TENANT_ID')
    
    if not all([client_id, client_secret, tenant_id]):
        print("❌ Missing credentials. Please set these environment variables:")
        if not client_id:
            print("   AZURE_CLIENT_ID (your App ID)")
        if not client_secret:
            print("   AZURE_CLIENT_SECRET (your Password)")  
        if not tenant_id:
            print("   AZURE_TENANT_ID (find using: az account show --query tenantId)")
        print()
        print("💡 Or add them to your .env file")
        return False
    
    print(f"✅ Client ID: {client_id[:8]}...")
    print(f"✅ Tenant ID: {tenant_id}")
    print("✅ Client Secret: [HIDDEN]")
    print()
    
    try:
        # Test authentication
        print("🔄 Testing authentication...")
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        
        # Try to get a token for Azure AI services
        token = credential.get_token("https://cognitiveservices.azure.com/.default")
        
        if token:
            print("🎉 SUCCESS! Service principal authentication works!")
            print(f"   Token expires: {token.expires_on}")
            return True
            
    except ClientAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print()
        print("💡 Possible issues:")
        print("   - Check your Client ID (App ID)")
        print("   - Check your Client Secret (Password)")
        print("   - Check your Tenant ID")
        print("   - Make sure the service principal has proper permissions")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def show_env_setup():
    """Show how to set up environment variables."""
    print("\n📝 To use these credentials in your app:")
    print("=" * 60)
    print("Add to your .env file:")
    print()
    print("AZURE_CLIENT_ID=your-app-id-here")
    print("AZURE_CLIENT_SECRET=your-password-here")
    print("AZURE_TENANT_ID=your-tenant-id-here")
    print()
    print("Or for GitHub Codespaces:")
    print("Repository Settings → Secrets and variables → Codespaces")

if __name__ == "__main__":
    success = test_service_principal()
    
    if success:
        print("\n🚀 Your service principal is ready to use!")
        print("   You can now run your Streamlit app")
    else:
        show_env_setup()
        print("\n🔧 Fix the issues above and try again")