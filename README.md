# CW2-AgenticAI-SriLanka-Banking-Trading

An enterprise-grade Agentic AI system designed for analyzing and trading Sri Lankan banking stocks. This project leverages CrewAI, unsupervised machine learning (K-Means), and the Gemini 2.5 Flash Large Language Model to simulate an autonomous institutional trading desk.

## Project Structure

├── data/                    # Raw and processed financial data (S3 connected)
├── notebooks/               # Jupyter notebooks for data engineering & ML
│   ├── 01_data_collection.ipynb     # CSE data fetching and AWS S3 upload
│   └── 02_data_preprocessing.ipynb  # Technical indicators & K-Means Clustering
├── agents/                  # AI agents for trading analysis
│   └── trading_agent.py     # CrewAI Multi-Agent decision engine
├── backtester.py            # Historical simulation & performance evaluation
├── requirements.txt         # Python dependencies
├── .env.example             # Template for Environment variables
└── README.md                # Project documentation


## Features
-Automated Data Engineering: Extraction and preprocessing of historical OHLCV data for CSE banking stocks, complete with cloud storage integration (AWS S3).

-Quantitative Segmentation: Unsupervised machine learning (K-Means Clustering) to categorize assets by their historical risk-return profiles.

-Agentic AI Workflow: A 4-agent CrewAI system (Data Analyst, Technical Analyst, Risk Manager, Trading Strategist) that collaboratively analyzes market conditions and strict risk parameters.

-Custom Tooling: Custom Python tools designed to chunk large CSV datasets, effectively bypassing LLM token limits and API rate exhaustion.

-Historical Backtesting: A time-series simulation engine to evaluate the AI's capital preservation and trading logic against historical data.

## Setup

1. **Clone and navigate to project**:

git clone [https://github.com/spideyjay/CW2-AgenticAI-SriLanka-Banking-Trading.git](https://github.com/spideyjay/CW2-AgenticAI-SriLanka-Banking-Trading.git)
cd CW2-AgenticAI-SriLanka-Banking-Trading


2. **Create virtual environment**:

# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate


3. **Install dependencies**:
pip install -r requirements.txt


4. **Configure environment**:
Rename .env.example to .env
Add your Google Gemini API Key (GEMINI_API_KEY=your_key_here)
Add your AWS Access Keys for cloud storage integration.

## Usage

### Phase 1 & 2: Data Pipeline & Machine Learning
1. **Run Data Collection & Preprocessing:**:

-Open and execute the Jupyter notebooks in order to fetch data, calculate technical indicators (MACD, RSI, SMA), and generate the K-Means risk clusters.

jupyter notebook notebooks/01_data_collection.ipynb
jupyter notebook notebooks/02_data_preprocessing.ipynb


### Phase 3: AI Trading Analysis

-Run the Multi-Agent system to get a real-time analysis of a specific asset based on the most recent 30 days of data:

python agents/trading_agent.py


### Phase 4: Backtesting Evaluation

-Run the historical simulation to test the AI's trading logic and capital preservation strategy over time:

python backtester.py


## Target Assets (Sri Lankan Banking Sector)

COMB.N0000.LK - Commercial Bank of Ceylon

HNB.N0000.LK - Hatton National Bank

NDB.N0000.LK - National Development Bank

BFLN.N0000.LK - Bank of Ceylon (BOC)

DFCC.N0000.LK - DFCC Bank

SAMP.N0000.LK - Sampath Bank


## Technologies Stack

-AI / LLM: CrewAI framework, Google Gemini 2.5 Flash, LangChain

-Machine Learning: Scikit-learn (K-Means Clustering)

-Data Engineering: Pandas, NumPy, yfinance

-Cloud Infrastructure: AWS S3 (Boto3)

-Visualization: Matplotlib, Seaborn

## Future Enhancements
- Core Banking Integration: Connect the AI Decision Engine directly to core banking system ledgers to verify institutional liquidity before simulated execution.

- Multi-Modal Sentiment Analysis: Upgrade the Data Analyst agent with NLP to ingest real-time CBSL policy announcements and financial news.

- Dynamic ML Recalibration: Automate the ML pipeline to dynamically update K-Means risk clusters based on shifting macroeconomic regimes.

## License
-This project is licensed under the MIT License - see the LICENSE file for details.