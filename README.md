# CW2-AgenticAI-SriLanka-Banking-Trading

An agentic AI system for analyzing and trading Sri Lankan banking stocks using CrewAI and advanced data analysis.

## Project Structure

```
├── data/                    # Raw and processed financial data
├── notebooks/              # Jupyter notebooks for analysis
│   ├── 01_data_collection.ipynb     # Data fetching and initial processing
│   └── 02_data_preprocessing.ipynb  # Technical indicators and cleaning
├── agents/                 # AI agents for trading analysis
│   └── trading_agent.py    # CrewAI-based trading analysis system
├── cloud/                  # Cloud deployment scripts (AWS)
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API keys)
└── README.md              # This file
```

## Features

- **Data Collection**: Automated fetching of OHLCV data for Sri Lankan banking stocks
- **Technical Analysis**: RSI, MACD, Moving Averages, Bollinger Bands
- **AI-Powered Analysis**: CrewAI agents for comprehensive market analysis
- **Risk Management**: Automated risk assessment and position sizing
- **Cloud Deployment**: AWS integration for scalable deployment

## Setup

1. **Clone and navigate to project**:
   ```bash
   cd "C:\Projects\CW2-AgenticAI-SriLanka-Banking-Trading"
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   - Copy `.env` and add your OpenAI API key
   - For AWS deployment, add AWS credentials

## Usage

### Data Analysis Pipeline

1. **Run data collection**:
   ```bash
   jupyter notebook notebooks/01_data_collection.ipynb
   ```
   - Fetches banking stock data
   - Handles API failures with sample data generation

2. **Run preprocessing**:
   ```bash
   jupyter notebook notebooks/02_data_preprocessing.ipynb
   ```
   - Adds technical indicators
   - Generates visualizations
   - Saves processed data

### AI Trading Analysis

Run the agentic analysis:
```bash
cd agents
python trading_agent.py
```

This will:
- Analyze stock data using multiple AI agents
- Provide technical analysis and trading signals
- Assess risks and recommend strategies

## Sri Lankan Banking Stocks

- COMB.N0000.LK - Commercial Bank of Ceylon
- HNB.N0000.LK - Hatton National Bank
- NDB.N0000.LK - National Development Bank
- BFLN.N0000.LK - Bank of Ceylon (BofC)
- DFCC.N0000.LK - DFCC Bank
- SAMP.N0000.LK - Sampath Bank

## Technologies Used

- **Python**: Core programming language
- **Pandas/NumPy**: Data manipulation and analysis
- **yfinance**: Financial data fetching
- **Matplotlib/Seaborn**: Data visualization
- **CrewAI**: Multi-agent AI framework
- **LangChain**: LLM integration
- **OpenAI GPT-4**: AI analysis engine
- **AWS Boto3**: Cloud services integration

## Next Steps

1. **Data Validation**: Replace sample data with real CSE data
2. **Model Training**: Implement ML models for price prediction
3. **Backtesting**: Create backtesting framework for strategies
4. **Live Trading**: Integrate with brokerage APIs
5. **Cloud Scaling**: Deploy agents on AWS Lambda/EC2

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

