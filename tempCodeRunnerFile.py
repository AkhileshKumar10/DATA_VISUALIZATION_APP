# backend.py
from flask import Flask, render_template, request, redirect, url_for
from datetime import timedelta
import pandas as pd
import plotly.express as px

app = Flask(__name__)
app.config['SERVER_NAME'] = '127.0.0.1:5000'  # Add this line
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)  # Add this line

data = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global data
    file = request.files['file']
    
    if file.filename.endswith('.csv'):
        data = pd.read_csv(file)
        return redirect(url_for('dashboard'))
    else:
        return "Invalid file format. Please upload a CSV file."

@app.route('/dashboard')
def dashboard():
    global data
    if data is None:
        return "No data available. Please upload a CSV file first."

    return render_template('dashboard.html', data_columns=data.columns)

@app.route('/plot', methods=['POST'])
def plot():
    global data
    if data is None:
        return "No data available. Please upload a CSV file."

    selected_columns = request.form.getlist('columns')
    chart_type = request.form.get('chart_type')

    if chart_type not in ['scatter', 'bar', 'line', 'pie']:
        return "Invalid chart type."

    if len(selected_columns) < 2:
        return "Please select at least two columns."

    try:
        if chart_type == 'scatter':
            fig = px.scatter(data, x=selected_columns[0], y=selected_columns[1], title=chart_type)
        elif chart_type == 'bar':
            fig = px.bar(data, x=selected_columns[0], y=selected_columns[1], title=chart_type)
        elif chart_type == 'line':
            fig = px.line(data, x=selected_columns[0], y=selected_columns[1], title=chart_type)
        elif chart_type == 'pie':
            fig = px.pie(data, names=selected_columns[0], values=selected_columns[1], title=chart_type)
        else:
            return "Invalid chart type."

        chart_json = fig.to_json()
        return render_template('plot.html', chart_json=chart_json, chart_type=chart_type)
    except Exception as e:
        return f"Error: {str(e)}. Please check selected columns and try again."

if __name__ == '__main__':
    app.run(debug=True)
