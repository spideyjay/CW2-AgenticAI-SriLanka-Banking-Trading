"""
Trading Agent for Sri Lanka Banking Stocks
Uses CrewAI to analyze stock data and provide trading recommendations
"""

import os
import pandas as pd
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai.tools import tool

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')

if not gemini_api_key:
    raise ValueError("Please set GEMINI_API_KEY in .env file")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    api_key=gemini_api_key,
    temperature=0.1
)

# --- CUSTOM TOOL TO PREVENT API RATE LIMITS ---
@tool("Read Recent Stock Data")
def get_recent_stock_data(ticker: str) -> str:
    """Reads the local CSV file and returns ONLY the last 30 days of technical data for a specific ticker."""
    try:
        # Read the file
        df = pd.read_csv('data/banking_processed.csv', header=[0, 1], index_col=0)
        df.index = pd.to_datetime(df.index)
        
        # Check if ticker exists
        if ticker not in df.columns.levels[0]:
            return f"Error: Ticker {ticker} not found in dataset."
            
        # Extract just that ticker's data and get the last 30 rows
        ticker_data = df[ticker].tail(30)
        
        # Return a small, focused string
        return ticker_data.to_csv()
    except Exception as e:
        return f"Error reading data: {str(e)}"

class BankingTradingAgent:
    def __init__(self):
        self.agents = {}
        self.tasks = {}
        self.crew = None
        self._setup_agents()

    def _setup_agents(self):
        """Set up the AI agents for trading analysis"""

        self.agents['data_analyst'] = Agent(
            role='Senior Data Analyst',
            goal='Analyze recent stock market data and identify patterns and trends',
            backstory="""You are a senior data analyst specializing in financial markets.
            You excel at looking at the last 30 days of trading data and identifying immediate 
            patterns that could indicate trading opportunities.""",
            llm=llm,
            tools=[get_recent_stock_data], # Uses our custom tool!
            verbose=True
        )

        self.agents['technical_analyst'] = Agent(
            role='Technical Analysis Expert',
            goal='Provide technical analysis and trading signals based on indicators',
            backstory="""You are a certified technical analyst with deep expertise in
            technical indicators like RSI, MACD, moving averages, and Bollinger Bands.""",
            llm=llm,
            verbose=True
        )

        self.agents['risk_manager'] = Agent(
            role='Risk Management Specialist',
            goal='Assess and manage trading risks, portfolio diversification',
            backstory="""You are a risk management expert who ensures trading strategies
            are safe and sustainable. You analyze volatility and recommend stop-loss levels.""",
            llm=llm,
            verbose=True
        )

        self.agents['trading_strategist'] = Agent(
            role='Trading Strategy Developer',
            goal='Develop comprehensive trading strategies based on analysis',
            backstory="""You are a trading strategist who combines technical analysis,
            risk management, and market insights to create profitable trading strategies.""",
            llm=llm,
            verbose=True
        )

    def create_analysis_tasks(self, ticker, cluster_label="Unknown"):
        """Create tasks for analyzing a specific stock"""

        self.tasks['data_analysis'] = Task(
            description=f"""Use the 'Read Recent Stock Data' tool to fetch the last 30 days of data for {ticker}.
            NOTE: A separate K-Means machine learning model has categorized this bank into Risk Cluster: {cluster_label}.
            Analyze the fetched data and provide:
            - Price trends over the last month
            - Notable anomalies
            - Current momentum direction""",
            agent=self.agents['data_analyst'],
            expected_output="A summary of the recent 30-day price trends and momentum."
        )

        self.tasks['technical_analysis'] = Task(
            description=f"""Review the data analysis for {ticker}. Provide buy/sell/hold signals based on 
            the technical indicators present in the recent data (RSI, MACD, etc).""",
            agent=self.agents['technical_analyst'],
            context=[self.tasks['data_analysis']],
            expected_output="Technical analysis report with clear trading signals."
        )

        self.tasks['risk_assessment'] = Task(
            description=f"""Assess the risk profile for {ticker} based on its Risk Cluster ({cluster_label}) 
            and recent volatility. Recommend specific stop-loss levels.""",
            agent=self.agents['risk_manager'],
            context=[self.tasks['data_analysis']],
            expected_output="Risk assessment with specific stop-loss recommendations."
        )

        self.tasks['strategy_development'] = Task(
            description=f"""Develop a final trading decision for {ticker} by synthesizing all previous analysis.
            You MUST output your final recommendation in the exact following structure:
            
            FINAL_DECISION: [BUY, SELL, or HOLD]
            CONFIDENCE_SCORE: [1-10]
            TARGET_PRICE: [Numeric value]
            STOP_LOSS: [Numeric value]
            RATIONALE: [One paragraph summary of why this decision was made]
            """,
            agent=self.agents['trading_strategist'],
            context=[self.tasks['data_analysis'], self.tasks['technical_analysis'], self.tasks['risk_assessment']],
            expected_output="A structured final decision containing exactly: FINAL_DECISION, CONFIDENCE_SCORE, TARGET_PRICE, STOP_LOSS, and RATIONALE."
        )

    def run_analysis(self, ticker, cluster_label="Unknown"):
        """Run the complete analysis for a ticker"""
        print(f"\nStarting analysis for {ticker} (Risk Cluster: {cluster_label})...")

        self.create_analysis_tasks(ticker, cluster_label)

        self.crew = Crew(
            agents=list(self.agents.values()),
            tasks=list(self.tasks.values()),
            verbose=True
        )

        result = self.crew.kickoff()
        return result

def main():
    agent = BankingTradingAgent()
    ticker = 'COMB.N0000.LK'
    
    # We pass the cluster label derived from our earlier K-Means analysis
    result = agent.run_analysis(ticker, cluster_label="Cluster 2 (Low Volatility, Positive Return)")
    
    print("\n" + "="*50)
    print("FINAL TRADING ANALYSIS RESULTS")
    print("="*50)
    print(result)

if __name__ == "__main__":
    main()