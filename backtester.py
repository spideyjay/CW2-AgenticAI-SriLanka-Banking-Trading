import os
import shutil
import pandas as pd
import time
import re
from agents.trading_agent import BankingTradingAgent

def run_backtest(ticker, initial_capital=100000):
    print("=" * 60)
    print(f"🚀 STARTING AGENTIC AI BACKTEST: {ticker}")
    print(f"💵 Initial Capital: {initial_capital:,.2f} LKR")
    print("=" * 60)

    # 1. Setup paths (Simulating "Time Travel")
    original_data_path = 'data/banking_processed.csv'
    backup_data_path = 'data/banking_processed_backup.csv'

    # Safely backup your hard-earned data!
    shutil.copy(original_data_path, backup_data_path)

    # Load the full dataset to map out our historical timeline
    full_df = pd.read_csv(backup_data_path, header=[0, 1], index_col=0)
    full_df.index = pd.to_datetime(full_df.index)

    # Select 4 historical evaluation points (Roughly once a month for the last 4 months)
    # We step backwards through the dataframe index to get valid trading days
    test_dates = full_df.index[-80::20] 

    capital = initial_capital
    shares = 0
    portfolio_history = []

    # Initialize your CrewAI Agent
    agent = BankingTradingAgent()

    try:
        for current_date in test_dates:
            date_str = current_date.strftime('%Y-%m-%d')
            print(f"\n📅 SIMULATING DATE: {date_str} " + "-"*30)

            # 2. Hide the Future: Slice data up to the simulated date
            sliced_df = full_df.loc[:current_date]

            # Overwrite the CSV so the Agent's tool only sees the past!
            sliced_df.to_csv(original_data_path)

            # Get the actual closing price on this simulated day
            current_price = sliced_df[ticker]['Close'].iloc[-1]
            print(f"📊 Market Close Price: {current_price:.2f} LKR")

            # 3. Wake up the Agents
            print("🧠 Agents analyzing market conditions...")
            
            # CRITICAL: Sleep for 15 seconds to prevent Google Gemini API Rate Limits!
            time.sleep(15) 
            
            # Pass the cluster label derived from your ML analysis
            result = agent.run_analysis(ticker, cluster_label="Cluster 2 (Low Volatility, Positive Return)")
            result_text = str(result)

            # 4. Parse the Decision using Regex
            decision_match = re.search(r'FINAL_DECISION:\s*(BUY|SELL|HOLD)', result_text, re.IGNORECASE)
            decision = decision_match.group(1).upper() if decision_match else "HOLD"

            print(f"🎯 AI DECISION: {decision}")

            # 5. Execute the Trade
            trade_action = "Held position"
            
            # Buy Logic: Go all in with available capital
            if decision == 'BUY' and capital >= current_price:
                shares_to_buy = int(capital // current_price)
                if shares_to_buy > 0:
                    capital -= shares_to_buy * current_price
                    shares += shares_to_buy
                    trade_action = f"Bought {shares_to_buy} shares"
            
            # Sell Logic: Liquidate all shares
            elif decision == 'SELL' and shares > 0:
                capital += shares * current_price
                trade_action = f"Sold {shares} shares"
                shares = 0

            portfolio_value = capital + (shares * current_price)
            print(f"💼 Action Taken: {trade_action}")
            print(f"💰 Current Portfolio Value: {portfolio_value:,.2f} LKR")

            # Log the metrics for the final report
            portfolio_history.append({
                'Date': date_str,
                'Price': round(current_price, 2),
                'Decision': decision,
                'Action': trade_action,
                'Value (LKR)': round(portfolio_value, 2)
            })

    except Exception as e:
        print(f"\n❌ Backtest crashed: {e}")
        
    finally:
        # 6. Clean Up: Always restore the original data file
        shutil.copy(backup_data_path, original_data_path)
        os.remove(backup_data_path)
        print("\n🧹 Cleaned up temporary files. Original dataset restored.")

    # 7. Print the Final Report
    print("\n" + "="*70)
    print("📈 AGENTIC BACKTEST FINAL REPORT")
    print("="*70)
    
    report_df = pd.DataFrame(portfolio_history)
    print(report_df.to_string(index=False))

    total_return = ((portfolio_value - initial_capital) / initial_capital) * 100
    
    print("-" * 70)
    if total_return >= 0:
        print(f"✅ FINAL PROFIT/LOSS: +{total_return:.2f}%")
    else:
        print(f"🔻 FINAL PROFIT/LOSS: {total_return:.2f}%")
    print("=" * 70)

if __name__ == '__main__':
    # Run the backtest for Commercial Bank starting with 100k LKR
    run_backtest('COMB.N0000.LK', initial_capital=100000)