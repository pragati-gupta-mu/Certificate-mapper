import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import BingGroundingTool
import json
import config

project_endpoint = config.PROJECT_ENDPOINT
conn_id = config.BING_CONNECTION_NAME
model_deployment = config.MODEL_DEPLOYMENT


project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
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
