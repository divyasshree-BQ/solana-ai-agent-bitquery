import anthropic
from rich import print

client = anthropic.Anthropic()

# Use your ngrok URL here
public_server_url = "https://40e881e091f9.ngrok-free.app"

response = client.beta.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Show me trending tokens"}
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

print(response.content)
