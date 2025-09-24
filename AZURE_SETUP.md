# Azure Service Principal Setup Guide

To use Azure AI Studio in Codespaces/Production, you need to create a service principal and get authentication credentials.

## If Someone Already Created a Service Principal for You

If you have:
- **App Name**: The display name of your application
- **App ID**: This is your `AZURE_CLIENT_ID` ✅
- **Password**: This is your `AZURE_CLIENT_SECRET` ✅

You still need the **Tenant ID**. Here's how to find it:

### Find Your Tenant ID:
```bash
# Using Azure CLI (easiest)
az account show --query tenantId --output tsv

# Or using PowerShell
(Get-AzContext).Tenant.Id
```

**Or via Azure Portal:**
1. Go to [Azure Portal](https://portal.azure.com)
2. Search for **Azure Active Directory**
3. In Overview → **Tenant ID** ✅

## Step 1: Create a Service Principal (Skip if you already have one)

### Option A: Using Azure Portal
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**
4. Name it something like "Certificate-Mapper-App"
5. Click **Register**
6. Note down:
   - **Application (client) ID** → This is your `AZURE_CLIENT_ID`
   - **Directory (tenant) ID** → This is your `AZURE_TENANT_ID`

### Option B: Using Azure CLI
```bash
az ad sp create-for-rbac --name "Certificate-Mapper-App" --role contributor
```

## Step 2: Create Client Secret
1. In your App registration, go to **Certificates & secrets**
2. Click **New client secret**
3. Add description and set expiration
4. Copy the **Value** → This is your `AZURE_CLIENT_SECRET`

## Step 3: Assign Permissions
1. Go to your Azure AI Studio resource
2. Navigate to **Access control (IAM)**
3. Click **Add role assignment**
4. Assign **Contributor** or **Cognitive Services User** role to your service principal

## Step 4: Add to GitHub Codespaces
1. Go to your GitHub repository
2. **Settings** → **Secrets and variables** → **Codespaces**
3. Add these secrets:
   - `AZURE_CLIENT_ID`
   - `AZURE_CLIENT_SECRET`
   - `AZURE_TENANT_ID`
   - `PROJECT_ENDPOINT` (you already have this)
   - `MODEL_DEPLOYMENT` (you already have this)
   - `SUBSCRIPTION_KEY` (you already have this)
   - `BING_CONNECTION_NAME` (you already have this)

## Step 5: Test
Run your application - it should now authenticate properly!

## Alternative: Find Your Tenant ID
If you need to find your tenant ID:
```bash
az account show --query tenantId --output tsv
```

Or in the Azure Portal:
- Azure Active Directory → Overview → Tenant ID