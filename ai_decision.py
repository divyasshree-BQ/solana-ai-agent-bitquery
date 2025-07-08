from openai import OpenAI
import os
from dotenv import load_dotenv
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)

def analyze_token_and_decide(token_data):
    prompt = (
        f"Analyze the following Solana token:\n"
        f"Name: {token_data['name']}\n"
        f"Symbol: {token_data['symbol']}\n"
        f"Market Cap: {token_data['market_cap']}\n"
        f"Liquidity (USD): {token_data['liquidity_usd']}\n"
        f"Volatility: {token_data['volatility']}\n"
        f"Top Holder Concentration (%): {token_data['holder_concentration']}\n"
        "\nBased on this data, decide whether to 'Buy', 'Avoid', or 'Hold'. Only reply with one word: Buy, Avoid, or Hold."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1,
            temperature=0
        )

        decision = response.choices[0].message.content.strip()
        return decision

    except Exception as e:
        print(f"Error from OpenAI API: {e}")
        return "Hold"