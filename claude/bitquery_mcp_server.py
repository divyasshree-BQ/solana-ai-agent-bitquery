import config
import bitquery_utils as bq
from mcp.server.fastmcp import FastMCP

WALLET_ADDRESS = config.WALLET_ADDRESS
mcp = FastMCP("BitQuery MCP Server")

@mcp.tool()
def get_trending_tokens():
    """Get trending cryptocurrency tokens."""
    return bq.get_trending_tokens()

@mcp.tool()
def get_wallet_balances():
    """Get wallet balances for configured wallet address."""
    return bq.get_wallet_balances(WALLET_ADDRESS)

@mcp.tool()
def get_marketcap(token_address: str):
    """Get market capitalization data for a token."""
    return bq.get_marketcap(token_address=token_address)

@mcp.tool()
def get_token_volatility(token_address: str):
    """Get volatility data for a token."""
    return bq.get_token_volatility(token_address=token_address)

@mcp.tool()
def get_top_liquidity_pools():
    """Get top liquidity pools."""
    return bq.get_top_liquidity_pools()

@mcp.tool()
def get_top_holders(token_address: str):
    """Get top holders for a token."""
    return bq.get_top_holders(token_address=token_address)

if __name__ == "__main__":
    mcp.run()
