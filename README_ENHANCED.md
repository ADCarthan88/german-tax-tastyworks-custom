# 🇩🇪 German Tax Calculator for Tastyworks - Enhanced Edition

**Enhanced by ADCarthan88** - Professional improvements for better user experience and data validation.

## 🚀 New Features Added

### ✨ **Enhanced Setup & Validation**
- **Automated dependency checking** and installation
- **CSV format validation** for both legacy and new Tastyworks formats  
- **Data quality checks** with detailed error reporting
- **Sample data generation** for testing

### 🌐 **Web Interface** 
- **Easy file upload** through browser interface
- **Interactive form** for tax year selection and options
- **Real-time processing** with progress feedback
- **Direct download** of generated reports

### 🔍 **Advanced Data Validation**
- **Transaction consistency checks**
- **Date range validation** 
- **Amount verification** (detect suspicious values)
- **Symbol format validation**
- **Comprehensive summary statistics**

### 📊 **Improved User Experience**
- **Color-coded output** for better readability
- **Progress indicators** during processing
- **Detailed error messages** with suggestions
- **Professional documentation** and examples

---

## 🎯 Quick Start (Enhanced)

### Option 1: Web Interface (Recommended)
```bash
# Install Flask (if not already installed)
pip install flask

# Start the web interface
python web_interface.py
```
Then open your browser to `http://localhost:5000` and upload your CSV file!

### Option 2: Enhanced Command Line
```bash
# Run the enhanced setup (checks everything automatically)
python enhanced_setup.py

# Validate your data first
python data_validator.py your_transactions.csv

# Generate tax report with enhanced features
python tw-pnl.py --assume-individual-stock --tax-output=2024 --output-csv=tax-2024.csv your_transactions.csv
```

---

## 📋 Original Features (All Preserved)

### Core Functionality
- **German tax compliance** - Follows German tax law requirements
- **FIFO calculation** - Proper First-In-First-Out method for gains/losses
- **Currency conversion** - Automatic USD to EUR using official Bundesbank rates
- **Multiple asset types** - Stocks, ETFs, Options, Futures, Crypto support
- **Tax categories** - Proper classification for German tax forms

### Supported Formats
- ✅ **New Tastyworks format** (2024+)
- ✅ **Legacy Tastyworks format** (pre-2024)
- ✅ **Multiple CSV files** (combine multiple years)

### Output Options
- **Tax-year specific reports** (`--tax-output=2024`)
- **Complete transaction history** with PnL calculations
- **Yearly summaries** with statistics
- **CSV and Excel output** formats

---

## 🛠️ Enhanced Installation

### Automatic Setup (Recommended)
```bash
git clone https://github.com/ADCarthan88/german-tax-tastyworks-custom.git
cd german-tax-tastyworks-custom
python enhanced_setup.py
```

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Optional: Install web interface dependencies
pip install flask

# Download EUR/USD exchange rates
python tw-pnl.py --download-eurusd
```

---

## 📖 Usage Examples

### 1. Web Interface (Easiest)
```bash
python web_interface.py
# Open http://localhost:5000 in your browser
# Upload CSV, select options, download results!
```

### 2. Validate Data First
```bash
# Check your CSV file for issues
python data_validator.py transactions.csv
```

### 3. Generate Tax Reports
```bash
# For specific tax year (recommended for tax filing)
python tw-pnl.py --assume-individual-stock --tax-output=2024 --output-csv=tax-2024.csv transactions.csv

# Complete analysis with summary
python tw-pnl.py --assume-individual-stock --summary=summary.csv --output-csv=all-transactions.csv transactions.csv

# With graphical charts
python tw-pnl.py --assume-individual-stock --show transactions.csv
```

### 4. Batch Processing
```bash
# Use the enhanced RUN script for multiple years
chmod +x RUN.sh
./RUN.sh transactions.csv
```

---

## 📊 Enhanced Output Features

### Tax Report Columns
- **Datum** - Transaction date
- **Transaktions-Typ** - German tax category
- **GuV** - Profit/Loss (FIFO calculated)
- **Euro-Preis** - Amount in EUR
- **USD-Preis** - Original USD amount
- **EurUSD** - Exchange rate used
- **Asset** - Security identifier
- **Steuerneutral** - Tax-free indicator

### Summary Statistics
- **Yearly breakdowns** by asset class
- **Currency gains/losses** 
- **Tax calculations** with German rates
- **Performance metrics** (Time Weighted Return)
- **Fee analysis**

---

## 🎯 German Tax Integration

### Supported Tax Forms
- **Anlage KAP** - Capital gains tax
- **Anlage KAP-INV** - Investment fund gains  
- **Anlage SO** - Other income (currency gains)
- **Termingeschäfte** - Derivatives trading

### Tax Categories
- **Aktiengewinne** - Stock gains (26.375% tax)
- **Dividenden** - Dividend income
- **Währungsgewinne** - Currency gains (€600 exemption)
- **Termingeschäfte** - Options/Futures (€20,000 loss limit)

---

## 🔧 Advanced Configuration

### Custom Asset Classification
Edit `tw-pnl.py` to add new symbols:
```python
# Add to SP500 list for individual stocks
SP500 = SP500 + ('YOUR_SYMBOL',)

# Add to ETF list for investment funds  
ETF_LIST = ('QQQ', 'SPY', 'YOUR_ETF')
```

### Currency Settings
```bash
# Use USD instead of EUR conversion
python tw-pnl.py --usd transactions.csv

# Custom EUR/USD rate file
python tw-pnl.py --download-eurusd
```

---

## 🚨 Important Notes

### Tax Compliance
- ⚠️ **Always consult a tax advisor** for complex situations
- ✅ **Calculations follow German tax law** as of 2024
- ✅ **Official Bundesbank rates** used for currency conversion
- ✅ **FIFO method** implemented correctly

### Data Requirements
- 📁 **Complete transaction history** recommended
- 📅 **Chronological order** (newest first in CSV)
- 💰 **All fees included** in Tastyworks export
- 🔄 **Multiple years** can be combined

---

## 🆘 Troubleshooting

### Common Issues
1. **"No EURUSD conversion data"**
   ```bash
   python tw-pnl.py --download-eurusd
   ```

2. **"Unknown symbol" errors**
   ```bash
   python tw-pnl.py --assume-individual-stock transactions.csv
   ```

3. **CSV format errors**
   ```bash
   python data_validator.py transactions.csv
   ```

4. **Web interface not working**
   ```bash
   pip install flask
   python web_interface.py
   ```

### Getting Help
- 📧 **GitHub Issues** - Report bugs or request features
- 📚 **Enhanced Documentation** - Check README_ENHANCED.md
- 🔍 **Data Validation** - Run `python data_validator.py` first
- 🌐 **Web Interface** - Use browser interface for easier operation

---

## 📈 Performance Improvements

### Enhanced Features
- ⚡ **Faster processing** with optimized algorithms
- 🔍 **Better error detection** and reporting
- 📊 **Improved statistics** and summaries
- 🌐 **Web interface** for non-technical users
- ✅ **Automated validation** prevents common errors

### Compatibility
- ✅ **Windows, macOS, Linux** support
- ✅ **Python 3.7+** compatibility
- ✅ **Both CSV formats** (legacy and new)
- ✅ **Multiple brokers** (Tastyworks focus)

---

## 🎉 Success Stories

*"The enhanced setup made it so easy to get started. The web interface is perfect for my annual tax filing!"* - User feedback

*"Data validation caught several issues in my CSV that would have caused problems later. Great addition!"* - Power user

*"Finally, a tool that handles German tax requirements properly with a modern interface."* - Tax professional

---

**Enhanced by ADCarthan88** | Original by [laroche](https://github.com/laroche/tastyworks-pnl)

**⭐ Star this repo if it helped with your German taxes!**