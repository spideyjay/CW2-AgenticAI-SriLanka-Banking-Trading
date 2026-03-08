"""
Comprehensive Trading Analysis for Sri Lankan Banking Stocks
Traditional Financial Analysis (No LLM Required)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class TraditionalTradingAnalysis:
    def __init__(self, data_path='data/simple_sample.csv'):
        self.data_path = data_path
        self.data = None
        self.analysis_results = {}

    def load_data(self):
        """Load and prepare the stock data"""
        try:
            self.data = pd.read_csv(self.data_path)
            self.data['Date'] = pd.to_datetime(self.data['Date'])
            self.data = self.data.sort_values('Date')
            print(f"Loaded {len(self.data)} days of data")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def calculate_technical_indicators(self):
        """Calculate key technical indicators"""
        if self.data is None:
            return False

        # Moving Averages
        self.data['SMA_20'] = self.data['Close'].rolling(window=20).mean()
        self.data['SMA_50'] = self.data['Close'].rolling(window=50).mean()
        self.data['EMA_12'] = self.data['Close'].ewm(span=12).mean()
        self.data['EMA_26'] = self.data['Close'].ewm(span=26).mean()

        # RSI
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.data['RSI'] = 100 - (100 / (1 + rs))

        # MACD
        self.data['MACD'] = self.data['EMA_12'] - self.data['EMA_26']
        self.data['Signal_Line'] = self.data['MACD'].ewm(span=9).mean()
        self.data['MACD_Histogram'] = self.data['MACD'] - self.data['Signal_Line']

        # Bollinger Bands
        self.data['BB_Middle'] = self.data['Close'].rolling(window=20).mean()
        self.data['BB_Upper'] = self.data['BB_Middle'] + 2 * self.data['Close'].rolling(window=20).std()
        self.data['BB_Lower'] = self.data['BB_Middle'] - 2 * self.data['Close'].rolling(window=20).std()

        # Volatility (ATR)
        high_low = self.data['High'] - self.data['Low']
        high_close = np.abs(self.data['High'] - self.data['Close'].shift())
        low_close = np.abs(self.data['Low'] - self.data['Close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        self.data['ATR'] = tr.rolling(window=14).mean()

        print("Technical indicators calculated successfully")
        return True

    def analyze_trends(self):
        """Analyze price trends and patterns"""
        if self.data is None:
            return {}

        recent_data = self.data.tail(60)  # Last 60 trading days (~3 months)

        # Trend Analysis
        current_price = recent_data['Close'].iloc[-1]
        price_30d_ago = recent_data['Close'].iloc[-30] if len(recent_data) >= 30 else recent_data['Close'].iloc[0]
        price_60d_ago = recent_data['Close'].iloc[0]

        price_change_30d = ((current_price - price_30d_ago) / price_30d_ago) * 100
        price_change_60d = ((current_price - price_60d_ago) / price_60d_ago) * 100

        # Moving Average Analysis
        sma_20 = recent_data['SMA_20'].iloc[-1]
        sma_50 = recent_data['SMA_50'].iloc[-1] if not pd.isna(recent_data['SMA_50'].iloc[-1]) else sma_20

        ma_signal = "BULLISH" if current_price > sma_20 > sma_50 else "BEARISH" if current_price < sma_20 < sma_50 else "NEUTRAL"

        # RSI Analysis
        current_rsi = recent_data['RSI'].iloc[-1]
        rsi_signal = "OVERBOUGHT" if current_rsi > 70 else "OVERSOLD" if current_rsi < 30 else "NEUTRAL"

        # MACD Analysis
        current_macd = recent_data['MACD'].iloc[-1]
        current_signal = recent_data['Signal_Line'].iloc[-1]
        macd_signal = "BULLISH" if current_macd > current_signal else "BEARISH"

        # Bollinger Band Analysis
        bb_upper = recent_data['BB_Upper'].iloc[-1]
        bb_lower = recent_data['BB_Lower'].iloc[-1]
        bb_position = (current_price - bb_lower) / (bb_upper - bb_lower)
        bb_signal = "NEAR UPPER BAND" if bb_position > 0.8 else "NEAR LOWER BAND" if bb_position < 0.2 else "MIDDLE RANGE"

        return {
            'current_price': current_price,
            'price_change_30d': price_change_30d,
            'price_change_60d': price_change_60d,
            'ma_signal': ma_signal,
            'rsi_value': current_rsi,
            'rsi_signal': rsi_signal,
            'macd_signal': macd_signal,
            'bb_position': bb_position,
            'bb_signal': bb_signal,
            'volatility': recent_data['ATR'].iloc[-1]
        }

    def calculate_statistics(self):
        """Calculate key statistical measures"""
        if self.data is None:
            return {}

        recent_data = self.data.tail(60)

        # Returns
        returns = recent_data['Close'].pct_change().dropna()
        daily_returns = returns.mean() * 100
        volatility = returns.std() * np.sqrt(252) * 100  # Annualized

        # Sharpe Ratio (assuming 3% risk-free rate)
        risk_free_rate = 0.03
        sharpe_ratio = (daily_returns/100 * 252 - risk_free_rate) / (volatility/100)

        # Maximum Drawdown
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min() * 100

        # Volume Analysis
        avg_volume = recent_data['Volume'].mean()
        volume_trend = "INCREASING" if recent_data['Volume'].tail(10).mean() > recent_data['Volume'].tail(20).head(10).mean() else "DECREASING"

        return {
            'daily_returns_pct': daily_returns,
            'annual_volatility_pct': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown_pct': max_drawdown,
            'avg_volume': avg_volume,
            'volume_trend': volume_trend
        }

    def generate_trading_recommendation(self):
        """Generate comprehensive trading recommendation"""
        if self.data is None:
            return {}

        trend_analysis = self.analyze_trends()
        statistics = self.calculate_statistics()

        # Scoring System (0-100 scale)
        score = 50  # Neutral starting point

        # Price Trend Score
        if trend_analysis['price_change_30d'] > 5:
            score += 15
        elif trend_analysis['price_change_30d'] < -5:
            score -= 15

        # Technical Indicators Score
        if trend_analysis['ma_signal'] == "BULLISH":
            score += 10
        elif trend_analysis['ma_signal'] == "BEARISH":
            score -= 10

        if trend_analysis['rsi_signal'] == "OVERSOLD":
            score += 15
        elif trend_analysis['rsi_signal'] == "OVERBOUGHT":
            score -= 15

        if trend_analysis['macd_signal'] == "BULLISH":
            score += 10
        elif trend_analysis['macd_signal'] == "BEARISH":
            score -= 10

        # Risk Assessment
        risk_level = "LOW" if statistics['annual_volatility_pct'] < 20 else "MEDIUM" if statistics['annual_volatility_pct'] < 35 else "HIGH"

        # Final Recommendation
        if score >= 70:
            recommendation = "STRONG BUY"
            confidence = "HIGH"
        elif score >= 55:
            recommendation = "BUY"
            confidence = "MEDIUM"
        elif score >= 45:
            recommendation = "HOLD"
            confidence = "MEDIUM"
        elif score >= 30:
            recommendation = "SELL"
            confidence = "MEDIUM"
        else:
            recommendation = "STRONG SELL"
            confidence = "HIGH"

        return {
            'recommendation': recommendation,
            'confidence': confidence,
            'score': score,
            'risk_level': risk_level,
            'stop_loss': trend_analysis['current_price'] * 0.95,  # 5% stop loss
            'take_profit': trend_analysis['current_price'] * 1.10,  # 10% take profit
            'time_horizon': "3-6 months"
        }

    def run_full_analysis(self):
        """Run the complete analysis pipeline"""
        print("🔍 Starting Comprehensive Trading Analysis for Sri Lankan Banking Stocks")
        print("=" * 80)

        if not self.load_data():
            return False

        if not self.calculate_technical_indicators():
            return False

        # Run all analyses
        trend_analysis = self.analyze_trends()
        statistics = self.calculate_statistics()
        recommendation = self.generate_trading_recommendation()

        # Store results
        self.analysis_results = {
            'trend_analysis': trend_analysis,
            'statistics': statistics,
            'recommendation': recommendation,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        return True

    def print_analysis_report(self):
        """Print comprehensive analysis report"""
        if not self.analysis_results:
            print("No analysis results available. Run analysis first.")
            return

        results = self.analysis_results

        print("\n📊 COMPREHENSIVE TRADING ANALYSIS REPORT")
        print("=" * 80)
        print(f"Analysis Date: {results['analysis_date']}")
        print(f"Stock: Sample Sri Lankan Banking Stock")
        print()

        # Current Market Data
        trend = results['trend_analysis']
        print("📈 CURRENT MARKET DATA:")
        print(f"Current Price: ${trend['current_price']:.2f}")
        print(f"30-Day Change: {trend['price_change_30d']:.1f}%")
        print(f"60-Day Change: {trend['price_change_60d']:.1f}%")
        print()

        # Technical Analysis
        print("🔧 TECHNICAL ANALYSIS:")
        print(f"Moving Average Signal: {trend['ma_signal']}")
        print(f"RSI Value: {trend['rsi_value']:.1f}")
        print(f"RSI Signal: {trend['rsi_signal']}")
        print(f"MACD Signal: {trend['macd_signal']}")
        print(f"Bollinger Band Position: {trend['bb_signal']}")
        print(f"Volatility (ATR): ${trend['volatility']:.2f}")
        print()

        # Statistical Analysis
        stats = results['statistics']
        print("📊 STATISTICAL ANALYSIS:")
        print(f"Daily Returns: {stats['daily_returns_pct']:.3f}%")
        print(f"Annual Volatility: {stats['annual_volatility_pct']:.1f}%")
        print(f"Sharpe Ratio: {stats['sharpe_ratio']:.2f}")
        print(f"Max Drawdown: {stats['max_drawdown_pct']:.1f}%")
        print(f"Average Volume: {stats['avg_volume']:,} shares")
        print(f"Volume Trend: {stats['volume_trend']}")
        print()

        # Trading Recommendation
        rec = results['recommendation']
        print("🎯 TRADING RECOMMENDATION:")
        print(f"Recommendation: {rec['recommendation']}")
        print(f"Confidence Level: {rec['confidence']}")
        print(f"Analysis Score: {rec['score']}/100")
        print(f"Risk Level: {rec['risk_level']}")
        print(f"Stop Loss: ${rec['stop_loss']:.2f}")
        print(f"Take Profit: ${rec['take_profit']:.2f}")
        print(f"Time Horizon: {rec['time_horizon']}")
        print()

        # Market Outlook
        print("🌟 MARKET OUTLOOK:")
        if rec['recommendation'] in ['STRONG BUY', 'BUY']:
            print("• Bullish momentum with positive technical indicators")
            print("• Favorable risk-reward ratio for long positions")
            print("• Consider accumulating on dips")
        elif rec['recommendation'] == 'HOLD':
            print("• Mixed signals suggest waiting for clearer direction")
            print("• Monitor key support/resistance levels")
            print("• Consider reducing position size if volatility increases")
        else:
            print("• Bearish pressure with negative technical divergence")
            print("• Risk management is crucial in current market conditions")
            print("• Consider defensive positioning or reducing exposure")

        print("\n⚠️  IMPORTANT DISCLAIMER:")
        print("This analysis is for educational purposes only and should not be considered")
        print("as financial advice. Always conduct your own research and consult with")
        print("qualified financial advisors before making investment decisions.")

if __name__ == "__main__":
    # Run the comprehensive analysis
    analyzer = TraditionalTradingAnalysis()
    if analyzer.run_full_analysis():
        analyzer.print_analysis_report()
    else:
        print("Analysis failed. Please check data and dependencies.")