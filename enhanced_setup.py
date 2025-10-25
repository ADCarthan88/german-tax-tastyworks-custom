#!/usr/bin/env python3
"""
Enhanced setup and validation script for German Tax Tastyworks Calculator
Customized by ADCarthan88 for improved user experience and data validation
"""

import os
import sys
import subprocess
import pandas as pd
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("[INFO] Checking dependencies...")
    
    required_packages = ['pandas', 'matplotlib']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"[OK] {package} - OK")
        except ImportError:
            missing_packages.append(package)
            print(f"[MISSING] {package} - MISSING")
    
    if missing_packages:
        print(f"\n[INSTALL] Installing missing packages: {', '.join(missing_packages)}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
        print("[SUCCESS] All dependencies installed successfully!")
    else:
        print("[SUCCESS] All dependencies are already installed!")

def validate_csv_format(csv_file):
    """Validate if the CSV file has the correct Tastyworks format"""
    print(f"\n[INFO] Validating CSV format: {csv_file}")
    
    if not os.path.exists(csv_file):
        print(f"[ERROR] File not found: {csv_file}")
        return False
    
    try:
        # Read first few lines to check format
        with open(csv_file, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        
        # Check for new format
        new_format_headers = ['Date', 'Type', 'Sub Type', 'Action', 'Symbol']
        # Check for legacy format  
        legacy_format_headers = ['Date/Time', 'Transaction Code', 'Transaction Subcode']
        
        if any(header in first_line for header in new_format_headers):
            print("[OK] New Tastyworks CSV format detected")
            return True
        elif any(header in first_line for header in legacy_format_headers):
            print("[OK] Legacy Tastyworks CSV format detected")
            return True
        else:
            print("[ERROR] Invalid CSV format. Please download from Tastyworks.")
            print("Expected headers not found in first line:")
            print(f"Found: {first_line}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error reading CSV file: {e}")
        return False

def create_sample_data():
    """Create sample data for testing"""
    print("\n[INFO] Creating sample test data...")
    
    sample_data = """Date,Type,Sub Type,Action,Symbol,Instrument Type,Description,Value,Quantity,Average Price,Commissions,Fees,Multiplier,Root Symbol,Underlying Symbol,Expiration Date,Strike Price,Call or Put,Order #,Currency
2024-01-03T14:00:00+0200,Money Movement,Deposit,,,,Wire Funds Received,"1,000.00",0,,--,0.00,,,,,,,,USD
2024-01-15T15:30:00+0200,Trade,Buy,BUY_TO_OPEN,AAPL,Equity,Bought 10 AAPL @ 150.00,"-1,500.00",10,150.00,1.00,0.00,1,AAPL,AAPL,,,,,USD
2024-02-16T23:00:00+0200,Money Movement,Credit Interest,,,,INTEREST ON CREDIT BALANCE,0.06,0,,--,0.00,,,,,,,,USD
2024-03-20T16:00:00+0200,Trade,Sell,SELL_TO_CLOSE,AAPL,Equity,Sold 10 AAPL @ 155.00,"1,550.00",10,155.00,1.00,0.00,1,AAPL,AAPL,,,,,USD"""
    
    sample_file = "sample_transactions.csv"
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(sample_data)
    
    print(f"[SUCCESS] Sample data created: {sample_file}")
    return sample_file

def run_test_calculation(csv_file):
    """Run a test calculation to verify everything works"""
    print(f"\n[INFO] Running test calculation with {csv_file}...")
    
    try:
        # Run with basic parameters using subprocess
        test_args = [
            'python', 'tw-pnl.py',
            '--assume-individual-stock',
            '--output-csv=test_output.csv',
            '--tax-output=2024',
            csv_file
        ]
        
        print("Running: " + " ".join(test_args))
        result = subprocess.run(test_args, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"[ERROR] Command failed with return code {result.returncode}")
            if result.stderr:
                print(f"[ERROR] {result.stderr}")
            return False
        
        if os.path.exists('test_output.csv'):
            print("[SUCCESS] Test calculation completed successfully!")
            print("[INFO] Output file created: test_output.csv")
            
            # Show first few lines of output
            with open('test_output.csv', 'r', encoding='utf-8') as f:
                lines = f.readlines()[:10]
                print("\n[INFO] Sample output:")
                for line in lines:
                    print(f"   {line.strip()}")
            
            return True
        else:
            print("[ERROR] Test calculation failed - no output file created")
            return False
            
    except Exception as e:
        print(f"[ERROR] Test calculation failed: {e}")
        return False

def main():
    """Main setup and validation function"""
    print("German Tax Tastyworks Calculator - Enhanced Setup")
    print("=" * 60)
    print("Customized by ADCarthan88 for improved user experience")
    print("=" * 60)
    
    # Step 1: Check dependencies
    check_dependencies()
    
    # Step 2: Check for existing CSV files
    csv_files = list(Path('.').glob('*.csv'))
    csv_files = [f for f in csv_files if f.name not in ['eurusd.csv', 'test_output.csv', 'sample_transactions.csv']]
    
    if csv_files:
        print(f"\n[INFO] Found existing CSV files:")
        for i, csv_file in enumerate(csv_files, 1):
            print(f"   {i}. {csv_file.name}")
        
        # Validate the first CSV file found
        if validate_csv_format(str(csv_files[0])):
            test_file = str(csv_files[0])
        else:
            print("[WARN] Creating sample data for testing instead...")
            test_file = create_sample_data()
    else:
        print("\n[INFO] No CSV files found in current directory")
        test_file = create_sample_data()
    
    # Step 3: Run test calculation
    if run_test_calculation(test_file):
        print("\n[SUCCESS] Setup completed successfully!")
        print("\n[INFO] Usage Examples:")
        print("   # Generate tax report for 2024:")
        print("   python tw-pnl.py --assume-individual-stock --tax-output=2024 --output-csv=tax-2024.csv your_file.csv")
        print("\n   # Generate complete summary:")
        print("   python tw-pnl.py --assume-individual-stock --summary=summary.csv --output-csv=all-transactions.csv your_file.csv")
        print("\n   # Show graphical analysis:")
        print("   python tw-pnl.py --assume-individual-stock --show your_file.csv")
    else:
        print("\n[ERROR] Setup encountered issues. Please check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())