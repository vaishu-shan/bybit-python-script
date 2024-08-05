import requests
import time
import hmac
import hashlib
import json

# Bybit API endpoints
BASE_URL = "https://api.bybit.com"
API_KEY = "ljPPmGuKxVmi9loRyh "
SECRET_KEY = "otllHPbpCrekibE16j8N4wEgIuWGGF5ApWMRy"

# Function to create API signature
def create_signature(params, secret_key):
    query_string = "&".join([f"{key}={value}" for key, value in sorted(params.items())])
    return hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()

# Function to make authenticated requests
def make_request(endpoint, params):
    params['api_key'] = API_KEY
    params['timestamp'] = int(time.time() * 1000)
    params['sign'] = create_signature(params, SECRET_KEY)

    max_retries = 5
    retry_count = 0
    wait_time = 5  # Initial wait time in seconds, start with a longer delay

    while retry_count < max_retries:
        response = requests.get(f"{BASE_URL}{endpoint}", params=params)

        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                print("Error: Failed to decode JSON response.")
                print(f"Raw response: {response.text}")
                return None
        elif response.status_code == 429:
            retry_count += 1
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                wait_time = int(retry_after)
            print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            wait_time *= 2  # Exponential backoff
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            return None

    print("Max retries reached. Exiting.")
    return None
    params['api_key'] = API_KEY
    params['timestamp'] = int(time.time() * 1000)
    params['sign'] = create_signature(params, SECRET_KEY)

    max_retries = 5
    retry_count = 0
    wait_time = 1  # Initial wait time in seconds

    while retry_count < max_retries:
        response = requests.get(f"{BASE_URL}{endpoint}", params=params)

        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                print("Error: Failed to decode JSON response.")
                print(f"Raw response: {response.text}")
                return None
        elif response.status_code == 429:
            retry_count += 1
            print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            wait_time *= 2  # Exponential backoff
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            return None

    print("Max retries reached. Exiting.")
    return None
# Function to get market prices
def get_market_data():
    endpoint = "/v2/public/tickers"
    params = {}
    data = make_request(endpoint, params)
    return data

# Function to identify arbitrage opportunities
def find_arbitrage_opportunities(market_data):
    # Implement your arbitrage logic here
    opportunities = []
    # Example: [(symbol1, symbol2, symbol3), ...]
    return opportunities

# Function to execute trades
def execute_trade(symbol, side, qty, price):
    endpoint = "/v2/private/order/create"
    params = {
        "symbol": symbol,
        "side": side,
        "order_type": "Limit",
        "qty": qty,
        "price": price,
        "time_in_force": "GoodTillCancel"
    }
    return make_request(endpoint, params)

# Function to transfer funds between subaccounts
def transfer_funds(from_subaccount, to_subaccount, amount):
    endpoint = "/v2/private/account/transfer"
    params = {
        "from_subaccount": from_subaccount,
        "to_subaccount": to_subaccount,
        "amount": amount
    }
    return make_request(endpoint, params)

# Main function
def main():
    initial_capital = 1000  # Initial capital in USD
    daily_profit_target = 0.1  # 10% profit target

    while True:
        # Step 1: Get market data
        market_data = get_market_data()

        # Step 2: Find arbitrage opportunities
        opportunities = find_arbitrage_opportunities(market_data)

        for opportunity in opportunities:
            symbol1, symbol2, symbol3 = opportunity

            # Step 3: Execute trades for the arbitrage opportunity
            # Example: Buy symbol1, sell symbol2, buy symbol3
            # Adjust the parameters as per the opportunity identified
            execute_trade(symbol1, "Buy", qty, price)
            execute_trade(symbol2, "Sell", qty, price)
            execute_trade(symbol3, "Buy", qty, price)

            # Step 4: Check if profit target is achieved
            current_profit = calculate_profit()
            if current_profit >= daily_profit_target:
                # Step 5: Transfer funds to subaccounts
                for subaccount in subaccounts:
                    transfer_funds(main_account, subaccount, necessary_amount)

        # Wait for some time before the next iteration
        time.sleep(60)

if __name__ == "__main__":
    main()
