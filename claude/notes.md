+------------------+       +-------------------+       +-----------------+
|  Bitquery API /  | --->  |  MCP Server       | --->  |  Claude (Code)  |
|  Solana Streams  |       | (SSE / HTTP / CLI)|       |   via Claude CLI|
+------------------+       +-------------------+       +-----------------+


```
python3 -m claude.bitquery_mcp_server

```

Simulate MCP Test

```
echo '{"method": "get_trending_tokens"}' | python3 claude/bitquery_mcp_server.py
```