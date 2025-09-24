import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
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

# Singleton pattern for agent creation
_agent_instance = None


def get_agent():
    """Get or create the singleton agent instance."""
    global _agent_instance
    if _agent_instance is None:
        with open("agent_instruction.md", "r") as f:
            instructions = f.read()
        _agent_instance = project_client.agents.create_agent(
            model=model_deployment,
            name="my-agent-certificate-mapper",
            instructions=instructions,
            tools=bing.definitions,
        )
        print(f"Created new agent with ID: {_agent_instance.id}")
    else:
        print(f"Reusing existing agent with ID: {_agent_instance.id}")
    return _agent_instance


def call_agent(row_dict):
    agent = get_agent()  # Get the singleton agent instance
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


def process_rows_with_progress(row_dicts, max_workers=5, progress_callback=None):
    """
    Process rows in parallel with progress tracking.
    
    Args:
        row_dicts: List of dictionaries, each representing a row
        max_workers: Maximum number of concurrent threads
        progress_callback: Function to call with progress updates (completed_count, total_count)
    
    Returns:
        List of results in the same order as input rows
    """
    results = [None] * len(row_dicts)
    completed = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_index = {
            executor.submit(call_agent, row_dict): idx 
            for idx, row_dict in enumerate(row_dicts)
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                print(f"Error processing row {idx}: {e}")
                row_dict = row_dicts[idx]
                results[idx] = {col: f"Error: {str(e)}" for col in row_dict.keys()}
            
            completed += 1
            if progress_callback:
                progress_callback(completed, len(row_dicts))
    
    return results
