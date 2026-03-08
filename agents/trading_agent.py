"""
Trading Agent for Sri Lanka Banking Stocks
Uses CrewAI to analyze stock data and provide trading recommendations
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import FileReadTool
from langchain_openai import ChatOpenAI
import pandas as pd

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    raise ValueError("Please set OPENAI_API_KEY in .env file")

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.1,
    api_key=openai_api_key
)

class BankingTradingAgent:
    def __init__(self, data_path='../data/banking_processed.csv'):
        self.data_path = data_path
        self.agents = {}
        self.tasks = {}
        self.crew = None
        self._setup_agents()

    def _setup_agents(self):
        """Set up the AI agents for trading analysis"""

        # Data Analyst Agent
        self.agents['data_analyst'] = Agent(
            role='Senior Data Analyst',
            goal='Analyze stock market data and identify patterns and trends',
            backstory="""You are a senior data analyst specializing in financial markets.
            You have 15+ years of experience analyzing stock data, technical indicators,
            and market trends. You excel at identifying patterns that could indicate
            trading opportunities.""",
            llm=llm,
            tools=[FileReadTool(file_path=self.data_path)],
            verbose=True
        )

        # Technical Analyst Agent
        self.agents['technical_analyst'] = Agent(
            role='Technical Analysis Expert',
            goal='Provide technical analysis and trading signals based on indicators',
            backstory="""You are a certified technical analyst with deep expertise in
            technical indicators like RSI, MACD, moving averages, and Bollinger Bands.
            You can identify support/resistance levels, trend patterns, and generate
            actionable trading signals.""",
            llm=llm,
            tools=[FileReadTool(file_path=self.data_path)],
            verbose=True
        )

        # Risk Manager Agent
        self.agents['risk_manager'] = Agent(
            role='Risk Management Specialist',
            goal='Assess and manage trading risks, portfolio diversification',
            backstory="""You are a risk management expert who ensures trading strategies
            are safe and sustainable. You analyze volatility, drawdown risks, and
            recommend position sizing and stop-loss levels.""",
            llm=llm,
            tools=[FileReadTool(file_path=self.data_path)],
            verbose=True
        )

        # Trading Strategist Agent
        self.agents['trading_strategist'] = Agent(
            role='Trading Strategy Developer',
            goal='Develop comprehensive trading strategies based on analysis',
            backstory="""You are a trading strategist who combines technical analysis,
            risk management, and market insights to create profitable trading strategies.
            You consider market conditions, risk tolerance, and investment goals.""",
            llm=llm,
            tools=[FileReadTool(file_path=self.data_path)],
            verbose=True
        )

    def create_analysis_tasks(self, ticker, analysis_period="3 months"):
        """Create tasks for analyzing a specific stock"""

        # Task 1: Data Analysis
        self.tasks['data_analysis'] = Task(
            description=f"""Analyze the processed data for {ticker} over the last {analysis_period}.
            Load the data from {self.data_path} and provide:
            - Price trends and volatility analysis
            - Key statistics (returns, volatility, correlations)
            - Any notable patterns or anomalies
            Focus on the most recent data and identify any significant changes.""",
            agent=self.agents['data_analyst'],
            expected_output="Comprehensive data analysis report with key insights and trends."
        )

        # Task 2: Technical Analysis
        self.tasks['technical_analysis'] = Task(
            description=f"""Perform technical analysis on {ticker} using indicators like:
            - RSI (overbought/oversold conditions)
            - MACD (momentum and trend signals)
            - Moving averages (SMA 20/50, EMA 12/26)
            - Bollinger Bands (volatility and price levels)
            Provide buy/sell/hold signals based on technical indicators.""",
            agent=self.agents['technical_analyst'],
            expected_output="Technical analysis report with clear trading signals and price targets."
        )

        # Task 3: Risk Assessment
        self.tasks['risk_assessment'] = Task(
            description=f"""Assess the risk profile for {ticker}:
            - Calculate Value at Risk (VaR)
            - Analyze maximum drawdown
            - Evaluate volatility metrics
            - Recommend position sizing and stop-loss levels
            - Suggest risk mitigation strategies""",
            agent=self.agents['risk_manager'],
            expected_output="Risk assessment report with quantitative risk metrics and mitigation recommendations."
        )

        # Task 4: Trading Strategy
        self.tasks['strategy_development'] = Task(
            description=f"""Develop a comprehensive trading strategy for {ticker} by combining:
            - Data analysis insights
            - Technical analysis signals
            - Risk management recommendations
            Create an actionable trading plan with:
            - Entry/exit criteria
            - Position sizing
            - Risk management rules
            - Performance expectations""",
            agent=self.agents['trading_strategist'],
            context=[self.tasks['data_analysis'], self.tasks['technical_analysis'], self.tasks['risk_assessment']],
            expected_output="Complete trading strategy with actionable recommendations."
        )

    def run_analysis(self, ticker, analysis_period="3 months"):
        """Run the complete analysis for a ticker"""
        print(f"Starting analysis for {ticker}...")

        # Create tasks
        self.create_analysis_tasks(ticker, analysis_period)

        # Create and run crew
        self.crew = Crew(
            agents=list(self.agents.values()),
            tasks=list(self.tasks.values()),
            verbose=True
        )

        # Execute the analysis
        result = self.crew.kickoff()

        return result

    def analyze_portfolio(self, tickers, analysis_period="3 months"):
        """Analyze multiple stocks for portfolio construction"""
        portfolio_analysis = {}

        for ticker in tickers:
            try:
                analysis = self.run_analysis(ticker, analysis_period)
                portfolio_analysis[ticker] = analysis
                print(f"Completed analysis for {ticker}")
            except Exception as e:
                print(f"Error analyzing {ticker}: {e}")
                portfolio_analysis[ticker] = f"Analysis failed: {e}"

        return portfolio_analysis

def main():
    """Main function to run the trading agent"""
    # Initialize agent
    agent = BankingTradingAgent()

    # Sri Lankan banking tickers
    tickers = ['COMB.N0000.LK', 'HNB.N0000.LK', 'NDB.N0000.LK']

    # Run analysis for one ticker first
    ticker = tickers[0]
    print(f"Analyzing {ticker}...")

    result = agent.run_analysis(ticker)
    print("\n" + "="*50)
    print("TRADING ANALYSIS RESULTS")
    print("="*50)
    print(result)

if __name__ == "__main__":
    main()