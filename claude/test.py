import anthropic
from rich import print
import config

# Ask user for input
user_input = input(" Ask Claude (MCP): ")

# Init Claude client
client = anthropic.Anthropic()

# Your ngrok-accessible MCP server URL
public_server_url = config.ngrok_url

# Send the prompt
response = client.beta.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": user_input}
    ],
    mcp_servers=[
        {
            "type": "url",
            "url": f"{public_server_url}/mcp/",
            "name": "bitquery-local",
        }
    ],
    extra_headers={
        "anthropic-beta": "mcp-client-2025-04-04"
    }
)

# Show result
print("\n Claude's Response:")
print(response.content)
