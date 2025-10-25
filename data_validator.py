#!/usr/bin/env python3
"""
Data Validator for Tastyworks CSV Files
Enhanced validation and data quality checks
Customized by ADCarthan88
"""

import pandas as pd
import sys
from datetime import datetime
import re

class TastyworksDataValidator:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.errors = []
        self.warnings = []
        self.df = None
        
    def validate_file_format(self):
        """Validate the CSV file format and structure"""
        try:
            # Try to read the file
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
            
            # Check for required headers
            new_format_headers = ['Date', 'Type', 'Sub Type', 'Action', 'Symbol', 'Value']
            legacy_format_headers = ['Date/Time', 'Transaction Code', 'Transaction Subcode', 'Amount']
            
            if any(header in first_line for header in new_format_headers):
                self.format_type = "new"
                return True
            elif any(header in first_line for header in legacy_format_headers):
                self.format_type = "legacy"
                return True
            else:
                self.errors.append("Invalid CSV format - missing required headers")
                return False
                
        except Exception as e:
            self.errors.append(f"Cannot read file: {e}")
            return False
    
    def load_data(self):
        """Load and parse the CSV data"""
        try:
            if self.format_type == "new":
                # New format - need to transform first
                from tw_pnl import transform_csv
                from io import StringIO
                transformed_data = transform_csv(self.csv_file)
                self.df = pd.read_csv(StringIO(transformed_data), parse_dates=['Date/Time'])
            else:
                # Legacy format
                self.df = pd.read_csv(self.csv_file, parse_dates=['Date/Time'])
            
            return True
        except Exception as e:
            self.errors.append(f"Error loading data: {e}")
            return False
    
    def validate_data_quality(self):
        """Perform comprehensive data quality checks"""
        if self.df is None:
            return False
        
        # Check for missing critical data
        critical_columns = ['Date/Time', 'Amount', 'Symbol']
        for col in critical_columns:
            if col in self.df.columns:
                missing_count = self.df[col].isna().sum()
                if missing_count > 0:
                    self.warnings.append(f"{missing_count} missing values in {col}")
        
        # Check date range
        if 'Date/Time' in self.df.columns:
            min_date = self.df['Date/Time'].min()
            max_date = self.df['Date/Time'].max()
            date_range = (max_date - min_date).days
            
            if date_range > 2000:  # More than ~5 years
                self.warnings.append(f"Large date range detected: {date_range} days ({min_date.date()} to {max_date.date()})")
            
            # Check for future dates
            future_dates = self.df[self.df['Date/Time'] > datetime.now()]
            if len(future_dates) > 0:
                self.warnings.append(f"{len(future_dates)} transactions have future dates")
        
        # Check for suspicious amounts
        if 'Amount' in self.df.columns:
            amounts = pd.to_numeric(self.df['Amount'], errors='coerce')
            
            # Very large amounts (> $1M)
            large_amounts = amounts[amounts.abs() > 1000000]
            if len(large_amounts) > 0:
                self.warnings.append(f"{len(large_amounts)} transactions with amounts > $1M")
            
            # Check for zero amounts where they shouldn't be
            zero_amounts = self.df[(amounts == 0) & (~self.df['Transaction Code'].isin(['Receive Deliver']))]
            if len(zero_amounts) > 0:
                self.warnings.append(f"{len(zero_amounts)} transactions with zero amounts")
        
        # Check symbol format
        if 'Symbol' in self.df.columns:
            symbols = self.df['Symbol'].dropna()
            
            # Check for unusual symbol formats
            unusual_symbols = symbols[~symbols.str.match(r'^[A-Z/]{1,10}$', na=False)]
            if len(unusual_symbols) > 0:
                unique_unusual = unusual_symbols.unique()[:5]  # Show first 5
                self.warnings.append(f"Unusual symbol formats detected: {list(unique_unusual)}")
        
        return True
    
    def validate_transaction_consistency(self):
        """Check for transaction consistency and logical errors"""
        if self.df is None:
            return False
        
        # Group by symbol and check for basic consistency
        if 'Symbol' in self.df.columns and 'Quantity' in self.df.columns:
            for symbol in self.df['Symbol'].dropna().unique():
                symbol_data = self.df[self.df['Symbol'] == symbol]
                
                # Check for fractional quantities in stocks (should be whole numbers)
                if not symbol.endswith('/USD'):  # Not crypto
                    quantities = pd.to_numeric(symbol_data['Quantity'], errors='coerce')
                    fractional = quantities[quantities % 1 != 0]
                    if len(fractional) > 0:
                        self.warnings.append(f"Fractional quantities found for {symbol}: {len(fractional)} transactions")
        
        return True
    
    def generate_summary_stats(self):
        """Generate summary statistics about the data"""
        if self.df is None:
            return {}
        
        stats = {
            'total_transactions': len(self.df),
            'date_range': None,
            'unique_symbols': 0,
            'transaction_types': {},
            'total_volume': 0
        }
        
        if 'Date/Time' in self.df.columns:
            min_date = self.df['Date/Time'].min()
            max_date = self.df['Date/Time'].max()
            stats['date_range'] = f"{min_date.date()} to {max_date.date()}"
        
        if 'Symbol' in self.df.columns:
            stats['unique_symbols'] = self.df['Symbol'].nunique()
        
        if 'Transaction Code' in self.df.columns:
            stats['transaction_types'] = self.df['Transaction Code'].value_counts().to_dict()
        
        if 'Amount' in self.df.columns:
            amounts = pd.to_numeric(self.df['Amount'], errors='coerce')
            stats['total_volume'] = abs(amounts).sum()
        
        return stats
    
    def run_full_validation(self):
        """Run complete validation suite"""
        print(f"🔍 Validating Tastyworks data: {self.csv_file}")
        print("=" * 60)
        
        # Step 1: File format validation
        if not self.validate_file_format():
            print("❌ File format validation failed")
            return False
        
        print(f"✅ File format: {self.format_type}")
        
        # Step 2: Load data
        if not self.load_data():
            print("❌ Data loading failed")
            return False
        
        print(f"✅ Data loaded: {len(self.df)} transactions")
        
        # Step 3: Data quality checks
        self.validate_data_quality()
        self.validate_transaction_consistency()
        
        # Step 4: Generate summary
        stats = self.generate_summary_stats()
        
        # Display results
        print("\n📊 Data Summary:")
        print(f"   Total transactions: {stats['total_transactions']:,}")
        print(f"   Date range: {stats['date_range']}")
        print(f"   Unique symbols: {stats['unique_symbols']}")
        print(f"   Total volume: ${stats['total_volume']:,.2f}")
        
        if stats['transaction_types']:
            print("\n📋 Transaction Types:")
            for ttype, count in stats['transaction_types'].items():
                print(f"   {ttype}: {count:,}")
        
        # Display warnings and errors
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"   • {error}")
            return False
        
        if not self.warnings:
            print("\n✅ No data quality issues detected!")
        
        print("\n🎯 Validation completed successfully!")
        return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python data_validator.py <tastyworks_file.csv>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    validator = TastyworksDataValidator(csv_file)
    
    success = validator.run_full_validation()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()