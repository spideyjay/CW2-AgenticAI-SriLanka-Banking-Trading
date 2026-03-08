#!/usr/bin/env python3
"""
Test script for CSE API Client
Tests the fallback mechanisms and data validation
"""

import sys
import os
sys.path.append('.')

from cse_api_client import CSEDataClient
import pandas as pd
from datetime import datetime, timedelta

def test_cse_client():
    """Test the CSE API client functionality"""
    print("🧪 Testing CSE API Client")
    print("=" * 40)

    # Initialize client
    client = CSEDataClient()

    # Test with a single ticker
    test_ticker = 'COMB.N0000.LK'
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')  # Last 30 days

    print(f"📊 Testing data fetch for {test_ticker}")
    print(f"📅 Date range: {start_date} to {end_date}")

    # Test data fetching
    df = client.fetch_with_fallback(test_ticker, start_date, end_date)

    if df is not None:
        print("✅ Data fetch successful!")
        print(f"📈 Data shape: {df.shape}")
        print(f"📅 Date range: {df.index.min()} to {df.index.max()}")
        print(f"💰 Latest price: ${df['Close'].iloc[-1]:.2f}")
        print(f"📊 Average volume: {df['Volume'].mean():,.0f}")

        # Test data validation
        is_valid = client.validate_data(df, test_ticker)
        print(f"🔍 Data validation: {'✅ PASSED' if is_valid else '❌ FAILED'}")

        # Show sample data
        print("\n📋 Sample data (last 5 days):")
        print(df.tail().to_string())

    else:
        print("❌ Data fetch failed - all APIs unavailable")

    print("\n🎯 Test completed!")

if __name__ == "__main__":
    test_cse_client()