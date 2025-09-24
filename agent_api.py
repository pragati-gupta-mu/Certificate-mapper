import json
import os
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import BingGroundingTool
import config

project_endpoint = config.PROJECT_ENDPOINT
conn_id = config.BING_CONNECTION_NAME
model_deployment = config.MODEL_DEPLOYMENT

# For Codespaces/local development, we need to use service principal auth
# You'll need to set these environment variables in GitHub Codespaces secrets:
# AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID

# Try to use environment variables for service principal authentication
environment = os.getenv("ENVIRONMENT")
print(f"Environment: {environment}")

# if environment == "local":
#     print("local environment detected, using DefaultAzureCredential")
#     # Use DefaultAzureCredential for local development
#     credential = DefaultAzureCredential()

# else:
client_id = os.getenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET') 
tenant_id = os.getenv('AZURE_TENANT_ID')

# Fallback to DefaultAzureCredential
credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=credential,
)

bing = BingGroundingTool(connection_id=conn_id)

with open("agent_instruction.md", "r") as f:
    instructions = f.read()
agent = project_client.agents.create_agent(
    model=model_deployment,
    name="my-agent-certificate-mapper",
    instructions=instructions,
    tools=bing.definitions,
)

def call_agent(row_dict):
    user_input_string = ", ".join(f"{k}: {v}" for k, v in row_dict.items())
    thread = project_client.agents.threads.create()
    project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input_string,
    )
    run = project_client.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id,
    )
    if run.status == "failed":
        return {col: "Run failed" for col in row_dict.keys()}
    messages = project_client.agents.messages.list(thread_id=thread.id)
    assistant_messages = [m for m in messages if m.role == "assistant"]
    if assistant_messages:
        try:
            message_formatted = assistant_messages[-1].content[0].text.value
            start = message_formatted.find('{')
            end = message_formatted.rfind('}') + 1
            json_str = message_formatted[start:end]
            return json.loads(json_str)
        except Exception:
            return {col: "Parse error" for col in row_dict.keys()}
    return {col: "No response" for col in row_dict.keys()}
