import asyncio
import threading
import time
import os
from dotenv import load_dotenv

from bitquery_utils import (
    get_trending_tokens,
    get_token_volatility,
    get_top_liquidity_pools,
    get_marketcap,
    get_wallet_balances,
    get_top_holders,
    subscribe_to_sol_trades
)
from ai_decision import analyze_token_and_decide

load_dotenv()

WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
BASE_TOKEN_MINT = os.getenv("BASE_TOKEN_MINT", "So11111111111111111111111111111111111111112")  # Example: SOL Mint

### ----------- AI Trading Loop ----------- ###

def ai_trading_loop():
    print("Starting AI Trading Loop...")

    while True:
        try:
            print("\nFetching trending tokens...")
            trending = get_trending_tokens()
            tokens = trending.get("data", {}).get("Solana", {}).get("DEXTradeByTokens", [])
            
            if not tokens:
                print("No trending tokens found.")
                time.sleep(30)
                continue

            print("Fetching wallet balances...")
            wallet_data = get_wallet_balances(WALLET_ADDRESS)
            balances = wallet_data.get("data", {}).get("Solana", {}).get("BalanceUpdates", [])

            owned_tokens_mint_addresses = set()
            for balance in balances:
                currency = balance.get("BalanceUpdate", {}).get("Currency", {})
                mint_address = currency.get("MintAddress")
                if mint_address:
                    owned_tokens_mint_addresses.add(mint_address)

            for token in tokens:
                currency = token["Trade"]["Currency"]
                mint = currency["MintAddress"]
                symbol = currency["Symbol"]
                name = currency["Name"]

                print(f"\nAnalyzing token: {symbol} ({name})")

                # Fetch additional token data
                marketcap_data = get_marketcap(mint)
                token_supply_updates = marketcap_data.get("data", {}).get("Solana", {}).get("TokenSupplyUpdates", [])
                if token_supply_updates:
                    marketcap = token_supply_updates[0].get("TokenSupplyUpdate", {}).get("PostBalanceInUSD", "Unknown")
                else:
                    marketcap = "Unknown"

                liquidity_data = get_top_liquidity_pools()
                volatility_data = get_token_volatility(mint, BASE_TOKEN_MINT)
                dex_trades = volatility_data.get("data", {}).get("Solana", {}).get("DEXTrades", [])
                if dex_trades:
                    volatility = dex_trades[0].get("volatility", "Unknown")
                else:
                    volatility = "Unknown"

                holders_data = get_top_holders(mint)
                holders = holders_data.get("data", {}).get("Solana", {}).get("BalanceUpdates", [])
                
                holder_concentration = "Unknown"
                if holders:
                    top_holder_balance = holders[0].get("Holding", 0)
                    total_balance = sum(h.get("Holding", 0) for h in holders)
                    if total_balance > 0:
                        holder_concentration = round(100 * top_holder_balance / total_balance, 2)

                # TODO: Parse liquidity_data to extract relevant liquidity in USD for this token
                liquidity_usd = "See liquidity_data output"

                wallet_holds_token = mint in owned_tokens_mint_addresses

                # AI Decision Making
                token_data = {
                    "name": name,
                    "symbol": symbol,
                    "mint_address": mint,
                    "market_cap": marketcap,
                    "liquidity_usd": liquidity_usd,
                    "volatility": volatility,
                    "holder_concentration": holder_concentration,
                    "wallet_holds_token": wallet_holds_token
                }

                decision = analyze_token_and_decide(token_data)
                print(f"AI Decision for {symbol}: {decision}")

                # Placeholder for trade execution logic
                if decision == "Buy":
                    if wallet_holds_token:
                        print(f"Already holding {symbol}, considering HOLD or additional BUY logic.")
                    else:
                        print(f"Would execute BUY for {symbol}")
                elif decision == "Sell":
                    if wallet_holds_token:
                        print(f"Would execute SELL for {symbol}")
                    else:
                        print(f"Cannot SELL {symbol}, wallet doesn't hold it.")
                elif decision == "Hold":
                    if wallet_holds_token:
                        print(f"Holding {symbol}.")
                    else:
                        print(f"Cannot HOLD {symbol}, wallet doesn't hold it.")
                elif decision == "Avoid":
                    print(f"Skipping {symbol} due to risk factors.")
                else:
                    print(f"Holding off on {symbol} for now.")

            time.sleep(60)  # Wait before re-evaluating

        except Exception as e:
            print(f"Error in trading loop: {e}")
            time.sleep(30)


### ----------- Stream Listener Example ----------- ###

async def run_trade_stream():
    print("Starting Solana DEX Trade Stream...")
    await subscribe_to_sol_trades()


### ----------- Entry Point ----------- ###

if __name__ == "__main__":
    try:
        # # Run trade stream in a separate thread
        # trade_stream_thread = threading.Thread(target=lambda: asyncio.run(run_trade_stream()), daemon=True)
        # trade_stream_thread.start()

        # Run AI Trading Loop (blocking)
        ai_trading_loop()

    except KeyboardInterrupt:
        print("Shutting down Trading Agent...")
