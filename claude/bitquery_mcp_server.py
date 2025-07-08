# claude/bitquery_mcp_server.py
import sys
import json
import os
import bitquery_utils as bq
import config

WALLET_ADDRESS = config.WALLET_ADDRESS

# Registry of allowed methods
METHODS = {
    "get_trending_tokens": bq.get_trending_tokens,
    "get_wallet_balances": lambda: bq.get_wallet_balances(WALLET_ADDRESS),
    "get_marketcap": bq.get_marketcap,
    "get_token_volatility": bq.get_token_volatility,
    "get_top_liquidity_pools": bq.get_top_liquidity_pools,
    "get_top_holders": bq.get_top_holders,
}

def main():
    for line in sys.stdin:
        try:
            input_data = json.loads(line)
            method_name = input_data.get("method")
            params = input_data.get("params", {})

            if method_name not in METHODS:
                raise ValueError(f"Unknown method: {method_name}")

            method = METHODS[method_name]

            # Call method with or without params
            if callable(method):
                if isinstance(params, dict):
                    result = method(**params) if params else method()
                else:
                    result = method()
            else:
                raise ValueError("Invalid method reference")

            sys.stdout.write(json.dumps({"result": result}) + "\n")
            sys.stdout.flush()

        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()