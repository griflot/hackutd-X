from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for
from calculate import calculateApproval
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg to avoid GUI issues
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

app = Flask(__name__)

data = pd.read_csv('HackUTD-2023-HomeBuyerInfo.csv')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Retrieve credit-related values from the form
        creditScore = float(request.form.get('creditScore'))
        grossIncome = float(request.form.get('grossIncome'))
        creditCardPayment = float(request.form.get('creditCardPaymentAmount'))
        studentLoanPayment = float(request.form.get('studentLoanPaymentAmount'))
        carPayment = float(request.form.get('carPaymentAmount'))
        monthlyMortgagePayment = float(request.form.get('mortgagePaymentAmount'))
        appraisedValue = float(request.form.get('appraisedValue'))
        downPayment = float(request.form.get('downPayment'))
        loanAmount = appraisedValue - downPayment

        result, valueOne, valueTwo = calculateApproval(
            creditScore, grossIncome, creditCardPayment, studentLoanPayment,
            carPayment, monthlyMortgagePayment, appraisedValue, downPayment, loanAmount
        )

        results = []
        for x in range(10):
            result = canBuyHouse(x)
            results.append((x, result))

        # Create a URL for the bar_graph endpoint with the data as parameters
        url = f'/bar_graph?income={grossIncome}&debt_payments={total_debt_payments}'

        return render_template('site.html', result=result, valueOne=valueOne, valueTwo=valueTwo, results=results, bar_graph_url=url)

    # This is the 'GET' request part of the route for rendering the initial form
    return render_template('site.html')

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

@app.route('/calculate_approval', methods=['POST'])
def sendCalculation():
    data = request.form  # Use request.form to get the form data
    result, loweredAppraisedValue, raisedDownPayment = calculateApproval(
        float(data['CreditScore']),
        float(data['GrossMonthlyIncome']),
        float(data['CreditCardPayment']),
        float(data['StudentLoanPayment']),
        float(data['CarPayment']),
        float(data['MonthlyMortgagePayment']),
        float(data['AppraisedValue']),
        float(data['DownPayment']),
        float(data['LoanAmount'])
    )

    confirmation_message = None
    if result == 1:
        confirmation_message = "Congratulations! You are likely to be approved for the loan."
    elif result == -1:
        confirmation_message = "Error in the given data. Please make sure the data is valid."
    elif result == -2:
        confirmation_message = "Your credit score is too low. Consider paying off credit cards on time."
    elif result == -3:
        confirmation_message = "Your Loan-to-Value (LTV) is too high. Consider a larger down payment or PMI."
    elif result == -4:
        confirmation_message = "Your Loan-to-Value (LTV) is too high. Consider a larger down payment."
    elif result == -5:
        confirmation_message = "Your Debt-to-Income (DTI) is too high. Consider a lower monthly mortgage rate."
    elif result == -6:
        confirmation_message = "Your Debt-to-Income (DTI) is too high. Consider transferring high-interest loans to low-interest credit cards."
    elif result == -7:
        confirmation_message = "Your Front-End Debt-to-Income (FEDTI) is too high. Consider a lower monthly mortgage rate."

    return render_template('site.html', confirmation_message=confirmation_message)

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
