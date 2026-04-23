import random
import time
import math

# Initial player setup
player = {
    "cash": 10000.00,  # Starting cash
    "portfolio": {},   # Stocks owned: {stock_name: [quantity, avg_buy_price]}
    "net_worth": 10000.00,
    "rank": "Novice Trader",
    "turn": 1  # Tracks turns for reference
}

# Stock market setup with initial prices
stocks = {
    "TechCorp": 150.00,
    "EnergyInc": 80.00,
    "HealthSys": 120.00,
    "AutoMotive": 60.00,
    "FinBank": 90.00
}

# Market events for dynamic price changes
market_events = [
    {"text": "TechCorp launches AI product!", "stock": "TechCorp", "impact": 0.15},
    {"text": "EnergyInc faces oil shortage.", "stock": "EnergyInc", "impact": -0.10},
    {"text": "HealthSys gets FDA approval!", "stock": "HealthSys", "impact": 0.20},
    {"text": "AutoMotive recalls vehicles.", "stock": "AutoMotive", "impact": -0.15},
    {"text": "FinBank raises rates.", "stock": "FinBank", "impact": 0.10},
    {"text": "Market boom!", "stock": None, "impact": 0.08},
    {"text": "Market crash!", "stock": None, "impact": -0.12}
]

# Trader ranks based on net worth
ranks = [
    (25000, "Pro Trader"),
    (50000, "Elite Trader"),
    (100000, "Market Legend")
]

# Transaction fee percentage
TRANSACTION_FEE = 0.005  # 0.5%

# Volatility settings for price fluctuations
volatility_settings = {
    "Low": 0.03,    # ±3% price changes
    "Medium": 0.05, # ±5% price changes
    "High": 0.08    # ±8% price changes
}

# Display welcome message
def display_welcome():
    print("\n" + "="*50)
    print("|| Welcome to the Stock Market Simulator!        ||")
    print("|| Trade stocks, harness AI insights,            ||")
    print("|| And become a Market Legend!                   ||")
    print("="*50 + "\n")
    time.sleep(2)

# Get volatility level from player
def get_volatility():
    print("Choose market volatility:")
    print("1. Low (Stable prices)")
    print("2. Medium (Moderate swings)")
    print("3. High (Wild fluctuations)")
    choice = input("Enter 1-3: ")
    if choice == "1":
        return "Low"
    elif choice == "2":
        return "Medium"
    elif choice == "3":
        return "High"
    else:
        print("Defaulting to Medium volatility.")
        time.sleep(1)
        return "Medium"

# Simulated AI stock tip
def get_stock_tip():
    stock = random.choice(list(stocks.keys()))
    trend = random.choice(["up", "down", "stable"])
    change = random.uniform(5, 15) if trend != "stable" else 0
    direction = "rise" if trend == "up" else "fall" if trend == "down" else "stay stable"
    return f"AI Tip: {stock} expected to {direction} by ~{change:.1f}%."

# Simulated AI news sentiment analysis
def get_news_sentiment():
    stock = random.choice(list(stocks.keys()))
    sentiment = random.choice(["Positive", "Neutral", "Negative"])
    change = random.uniform(5, 20) if sentiment != "Neutral" else 0
    direction = "rise" if sentiment == "Positive" else "fall" if sentiment == "Negative" else "stay stable"
    return f"AI Sentiment Analysis: {sentiment} sentiment for {stock} (may {direction} by ~{change:.1f}%)."

# Trigger random market event
def trigger_market_event():
    if random.random() < 0.3:  # 30% chance per turn
        event = random.choice(market_events)
        print("\n" + "*"*40)
        print(f"Market News: {event['text']}")
        print("*"*40)
        if event["stock"]:
            stocks[event["stock"]] *= (1 + event["impact"])
            stocks[event["stock"]] = round(stocks[event["stock"]], 2)
        else:
            for stock in stocks:
                stocks[stock] *= (1 + event["impact"])
                stocks[stock] = round(stocks[stock], 2)
        time.sleep(2)

# Update stock prices with random fluctuations
def update_stock_prices(volatility):
    for stock in stocks:
        change_percent = random.uniform(-volatility_settings[volatility], volatility_settings[volatility])
        stocks[stock] *= (1 + change_percent)
        stocks[stock] = round(stocks[stock], 2)

# Calculate net worth
def calculate_net_worth():
    portfolio_value = sum(
        qty * stocks[stock] for stock, [qty, _] in player["portfolio"].items()
    )
    player["net_worth"] = player["cash"] + portfolio_value
    return round(player["net_worth"], 2)

# Update player rank based on net worth
def update_rank():
    net_worth = calculate_net_worth()
    for threshold, rank in ranks:
        if net_worth >= threshold and player["rank"] != rank:
            print("\n" + "="*40)
            print(f"Congratulations! You've been promoted to {rank}!")
            print("="*40)
            player["rank"] = rank
            time.sleep(2)

# Display professional header
def display_header():
    print("\n" + "="*50)
    print(f"|| Stock Market Simulator - Turn {player['turn']} ||")
    print(f"|| Rank: {player['rank']} ||")
    print("="*50 + "\n")

# Display market data with numbered options
def display_market():
    print("-"*40)
    print("||           Current Market Prices          ||")
    print("-"*40)
    stock_list = list(stocks.keys())
    for i, stock in enumerate(stock_list, 1):
        print(f"{i}. {stock:<13} | ${stocks[stock]:>8.2f}")
    print("-"*40 + "\n")
    return stock_list

# Display player portfolio
def display_portfolio():
    print("-"*40)
    print("||           Your Portfolio                 ||")
    print("-"*40)
    print(f"Cash Balance: ${player['cash']:.2f}")
    print(f"Net Worth: ${calculate_net_worth():.2f}")
    print("\nStocks Owned:")
    if not player["portfolio"]:
        print("No stocks owned.")
    else:
        print(f"{'Stock':<15} | {'Qty':>5} | {'Avg Buy Price':>12} | {'Current Value':>12}")
        for stock, [qty, avg_price] in player["portfolio"].items():
            current_value = qty * stocks[stock]
            print(f"{stock:<15} | {qty:>5} | ${avg_price:>10.2f} | ${current_value:>10.2f}")
    print("-"*40 + "\n")

# Select stock by number
def select_stock(prompt, stock_list):
    try:
        choice = input(prompt)
        if choice.lower() == "cancel":
            return None
        choice_num = int(choice)
        if 1 <= choice_num <= len(stock_list):
            return stock_list[choice_num - 1]
        else:
            print(f"Invalid number! Choose 1 to {len(stock_list)}.")
            time.sleep(1)
            return None
    except ValueError:
        print("Invalid input! Enter a number or 'cancel'.")
        time.sleep(1)
        return None

# Buy stock
def buy_stock():
    stock_list = display_market()
    prompt = f"Enter stock number to buy (1-{len(stock_list)}, or 'cancel' to go back): "
    stock = select_stock(prompt, stock_list)
    if not stock:
        return
    
    try:
        qty = int(input(f"Enter quantity to buy ({stock} @ ${stocks[stock]:.2f}): "))
        if qty <= 0:
            print("Quantity must be positive!")
            time.sleep(1)
            return
        total_cost = qty * stocks[stock]
        fee = total_cost * TRANSACTION_FEE
        total_with_fee = total_cost + fee
        if total_with_fee > player["cash"]:
            print("Insufficient funds (including 0.5% fee)!")
            time.sleep(1)
            return
        
        # Update portfolio
        player["cash"] -= total_with_fee
        if stock in player["portfolio"]:
            curr_qty, curr_avg = player["portfolio"][stock]
            new_qty = curr_qty + qty
            new_avg = ((curr_qty * curr_avg) + (qty * stocks[stock])) / new_qty
            player["portfolio"][stock] = [new_qty, new_avg]
        else:
            player["portfolio"][stock] = [qty, stocks[stock]]
        print(f"Bought {qty} shares of {stock} for ${total_cost:.2f} + ${fee:.2f} fee.")
        time.sleep(1)
    except ValueError:
        print("Invalid quantity!")
        time.sleep(1)

# Sell stock
def sell_stock():
    display_portfolio()
    if not player["portfolio"]:
        print("No stocks to sell!")
        time.sleep(1)
        return
    stock_list = list(player["portfolio"].keys())
    print("Stocks you own:")
    for i, stock in enumerate(stock_list, 1):
        print(f"{i}. {stock}")
    prompt = f"Enter stock number to sell (1-{len(stock_list)}, or 'cancel' to go back): "
    stock = select_stock(prompt, stock_list)
    if not stock:
        return
    
    try:
        qty = int(input(f"Enter quantity to sell ({stock} @ ${stocks[stock]:.2f}): "))
        if qty <= 0:
            print("Quantity must be positive!")
            time.sleep(1)
            return
        if qty > player["portfolio"][stock][0]:
            print("You don't own enough shares!")
            time.sleep(1)
            return
        
        # Update portfolio
        total_earned = qty * stocks[stock]
        fee = total_earned * TRANSACTION_FEE
        total_after_fee = total_earned - fee
        player["cash"] += total_after_fee
        player["portfolio"][stock][0] -= qty
        if player["portfolio"][stock][0] == 0:
            del player["portfolio"][stock]
        print(f"Sold {qty} shares of {stock} for ${total_earned:.2f} - ${fee:.2f} fee.")
        time.sleep(1)
    except ValueError:
        print("Invalid quantity!")
        time.sleep(1)

# Main game loop
def main():
    # Display welcome message
    display_welcome()
    # Get volatility setting
    volatility = get_volatility()
    
    while True:
        trigger_market_event()
        update_stock_prices(volatility)
        update_rank()
        display_header()
        print("1. View Market Prices")
        print("2. View Portfolio")
        print("3. Buy Stock")
        print("4. Sell Stock")
        print("5. Get AI Stock Tip")
        print("6. Get AI News Sentiment")
        print("7. Exit Portfolio")
        print("-"*50)
        
        choice = input("Select an option (1-7): ")
        
        if choice == "1":
            display_market()
            input("Press Enter to continue...")
        elif choice == "2":
            display_portfolio()
            input("Press Enter to continue...")
        elif choice == "3":
            buy_stock()
        elif choice == "4":
            sell_stock()
        elif choice == "5":
            print("\n" + get_stock_tip())
            input("Press Enter to continue...")
        elif choice == "6":
            print("\n" + get_news_sentiment())
            input("Press Enter to continue...")
        elif choice == "7":
            print("\n" + "="*50)
            print("||          Thank you for Trading!          ||")
            print(f"|| Final Net Worth: ${calculate_net_worth():.2f} ||")
            print(f"|| Final Rank: {player['rank']} ||")
            print("="*50)
            break
        else:
            print("Invalid option!")
            time.sleep(1)
        
        player["turn"] += 1

# Start the game
if __name__ == '__main__':
    main()
  