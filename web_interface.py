#!/usr/bin/env python3
"""
Web Interface for German Tax Tastyworks Calculator
Simple Flask web app for easy file upload and tax calculation
Customized by ADCarthan88
"""

try:
    from flask import Flask, request, render_template_string, send_file, flash, redirect, url_for
    import os
    import tempfile
    from werkzeug.utils import secure_filename
    import tw_pnl
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>German Tax Calculator for Tastyworks</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .form-group { margin-bottom: 15px; }
        .form-control { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        .btn { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .btn:hover { background: #2980b9; }
        .alert { padding: 15px; margin-bottom: 20px; border-radius: 4px; }
        .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .alert-error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }
        .feature { background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #3498db; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🇩🇪 German Tax Calculator for Tastyworks</h1>
        <p>Enhanced by ADCarthan88 - Upload your Tastyworks CSV and generate German tax reports</p>
    </div>

    {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-success">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <div class="features">
        <div class="feature">
            <h3>📊 Tax Reports</h3>
            <p>Generate compliant German tax reports for specific years</p>
        </div>
        <div class="feature">
            <h3>💱 Currency Conversion</h3>
            <p>Automatic USD to EUR conversion using official Bundesbank rates</p>
        </div>
        <div class="feature">
            <h3>📈 FIFO Calculation</h3>
            <p>Proper FIFO method for realized gains and losses</p>
        </div>
        <div class="feature">
            <h3>📋 Multiple Formats</h3>
            <p>Supports both legacy and new Tastyworks CSV formats</p>
        </div>
    </div>

    <form method="post" enctype="multipart/form-data">
        <div class="form-group">
            <label for="file"><strong>Upload Tastyworks CSV File:</strong></label>
            <input type="file" name="file" id="file" class="form-control" accept=".csv" required>
            <small>Download your transaction history from Tastyworks as CSV</small>
        </div>

        <div class="form-group">
            <label for="tax_year"><strong>Tax Year (optional):</strong></label>
            <select name="tax_year" id="tax_year" class="form-control">
                <option value="">All Years (Complete Report)</option>
                <option value="2024">2024</option>
                <option value="2023">2023</option>
                <option value="2022">2022</option>
                <option value="2021">2021</option>
                <option value="2020">2020</option>
            </select>
        </div>

        <div class="form-group">
            <label>
                <input type="checkbox" name="assume_stock" checked> 
                Assume unknown symbols are individual stocks
            </label>
        </div>

        <div class="form-group">
            <label>
                <input type="checkbox" name="include_summary"> 
                Include yearly summary report
            </label>
        </div>

        <button type="submit" class="btn">🧮 Calculate Tax Report</button>
    </form>

    <div style="margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
        <h3>📚 How to Use:</h3>
        <ol>
            <li>Download your transaction history from Tastyworks as CSV</li>
            <li>Upload the file using the form above</li>
            <li>Select your preferred tax year (or leave blank for all years)</li>
            <li>Click "Calculate Tax Report" to generate your German tax documents</li>
            <li>Download the generated CSV file for use in your tax software</li>
        </ol>
        
        <h3>⚠️ Important Notes:</h3>
        <ul>
            <li>This tool calculates taxes according to German tax law</li>
            <li>Currency gains are computed using FIFO method</li>
            <li>Official EUR/USD rates from Bundesbank are used</li>
            <li>Always consult with a tax advisor for complex situations</li>
        </ul>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                
                # Get form parameters
                tax_year = request.form.get('tax_year')
                assume_stock = 'assume_stock' in request.form
                include_summary = 'include_summary' in request.form
                
                # Generate output filename
                base_name = filename.rsplit('.', 1)[0]
                if tax_year:
                    output_filename = f"{base_name}_tax_{tax_year}.csv"
                else:
                    output_filename = f"{base_name}_tax_report.csv"
                
                output_path = os.path.join(UPLOAD_FOLDER, output_filename)
                
                # Prepare arguments for tw_pnl
                args = []
                if assume_stock:
                    args.append('--assume-individual-stock')
                if tax_year:
                    args.append(f'--tax-output={tax_year}')
                args.append(f'--output-csv={output_path}')
                
                if include_summary:
                    summary_path = os.path.join(UPLOAD_FOLDER, f"{base_name}_summary.csv")
                    args.append(f'--summary={summary_path}')
                
                args.append(filepath)
                
                # Run the calculation
                tw_pnl.main(args)
                
                flash(f'Tax report generated successfully! Download: {output_filename}')
                return send_file(output_path, as_attachment=True, download_name=output_filename)
                
            except Exception as e:
                flash(f'Error processing file: {str(e)}')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload a CSV file.')
            return redirect(request.url)
    
    return render_template_string(HTML_TEMPLATE)

def main():
    if not FLASK_AVAILABLE:
        print("Flask is not installed. Install it with: pip install flask")
        print("Or run the command-line version directly with: python tw-pnl.py")
        return
    
    print("🌐 Starting German Tax Calculator Web Interface...")
    print("📍 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()