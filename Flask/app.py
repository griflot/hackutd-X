from flask import Flask, render_template, request, send_file
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg to avoid GUI issues
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

app = Flask(__name__)

data = pd.read_csv('HackUTD-2023-HomeBuyerInfo.csv')

@app.route('/')
def home():
    results = []
    for x in range(10):
        result = canBuyHouse(x)
        results.append((x, result))

    gross_income = 0
    total_debt_payments = 0

    # Create a URL for the bar_graph endpoint with the data as parameters
    url = f'/bar_graph?income={gross_income}&debt_payments={total_debt_payments}'

    return render_template('site.html', results=results, bar_graph_url=url)

@app.route('/bar_graph')
def bar_graph():
    # Retrieve gross income and total debt payments from URL parameters
    gross_income = float(request.args.get('income'))
    total_debt_payments = float(request.args.get('debt_payments'))

    # Check if both values are zero (empty chart)
    if gross_income == 0 and total_debt_payments == 0:
        return "Chart is empty"

    # Create a bar graph
    img = BytesIO()
    fig, ax = plt.subplots(figsize=(8, 4))
    categories = ['Gross Income', 'Total Debt Payments']
    values = [gross_income, total_debt_payments]
    ax.bar(categories, values, width=0.5)
    plt.ylabel('Amount')
    plt.title('Income vs. Debt Payments')

    plt.savefig(img, format='png')
    img.seek(0)

    # Save the image to the 'static' folder
    plot_filename = os.path.join('static', 'bar_graph.png')
    with open(plot_filename, 'wb') as plot_file:
        plot_file.write(img.read())

    # Serve the saved image
    return send_file(plot_filename, mimetype='image/png')

def canBuyHouse(id):
    currAcc = data.iloc[id]
    if currAcc.get("CreditScore") < 640:
        return -4
    if calcLTV(currAcc.get("LoanAmount"), currAcc.get("AppraisedValue")) > 80:
        return -3
    if calcDTI(
        currAcc.get("GrossMonthlyIncome"),
        currAcc.get("CarPayment"),
        currAcc.get("CreditCardPayment"),
        currAcc.get("MonthlyMortgagePayment"),
    ) > 43:
        return -2
    if calcFEDTI(currAcc.get("GrossMonthlyIncome"), currAcc.get("MonthlyMortgagePayment")) > 28:
        return -1
    return 10

def calcLTV(loan, value):
    return (loan / value) * 100

def calcDTI(income, car, creditCard, mortgage):
    loss = car + creditCard + mortgage
    return (loss / income) * 100

def calcFEDTI(income, mortgage):
    return (mortgage / income) * 100

if __name__ == '__main__':
   app.run()
