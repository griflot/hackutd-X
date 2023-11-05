# testing file with core changes to calculate logic

def LTVCalc(loan, value):
    return (loan/value)*100
def DTICalc(loss, pay):
    return (loss/pay)*100
def FEDTICalc(mortgage, loss):
    return (mortgage/loss)*100
def maxAcceptableValue(pay):
    return pay/.2
def minAcceptableDownpay(value):
    return value*0.2
def maxMortgage(loss):
    return loss*0.45

'''
return codes:
    1: likely to be approved
    -1: credit score too low: advise to pay off credit cards on time
    -2: LTV too high, might qualify with PMI: advise to either choose a larger down payment or purchase PMI (private mortgage insurance)
    -3: LTV too high: advise to choose a larger down payment
    -4: DTI too high, might qualify in some scenarios (which ones???)
    -5: DTI too high: advise to transfer high interest loans to low interest credit cards (but not have too many credit cards either)
    -6: FEDTI too high
    -7: error in given data
'''
def calculateApproval(CreditScore, GrossMonthlyIncome, CreditCardPayment, StudentLoanPayment, CarPayment, MonthlyMortgagePayment, AppraisedValue, DownPayment, LoanAmount):
    if LoanAmount + DownPayment != AppraisedValue or MonthlyMortgagePayment > LoanAmount:
        print("invalid data given: value constraints not met")
        return -7
    
    if CreditScore < 0 or GrossMonthlyIncome < 0 or CreditCardPayment < 0 or StudentLoanPayment < 0 or CarPayment < 0 or MonthlyMortgagePayment < 0 or AppraisedValue < 0 or DownPayment < 0 or LoanAmount < 0:
        print("invalid data given: data contains negative values")
        return -7

    Credit_Pass = CreditScore > 640
    LTV_Pass = ((LoanAmount/AppraisedValue)*100) < 80
    DTI_Pass = ((CarPayment+StudentLoanPayment+CreditCardPayment+MonthlyMortgagePayment)/GrossMonthlyIncome)*100 < 36 and MonthlyMortgagePayment / (MonthlyMortgagePayment + CreditCardPayment + CarPayment + StudentLoanPayment) * 100 <= 28
    FEDTI_Pass = (MonthlyMortgagePayment/GrossMonthlyIncome)*100 <= 28
    
    if ~Credit_Pass:
        print("Pay off debt etc etc")
        return -1
    elif ~LTV_Pass:
        print("you got a LTV problem")
        if LTVCalc(LoanAmount, AppraisedValue) < 95:
            print("max acctpable price: " + str(maxAcceptableValue(DownPayment)))
            print("min accptable down payment: " + str(minAcceptableDownpay(AppraisedValue)))
            return -2
        else:
            print("absolutly not")
            return -3
    elif ~DTI_Pass:
        print("you got a dti problm")
        if DTICalc(CarPayment + CreditCardPayment + StudentLoanPayment + MonthlyMortgagePayment, GrossMonthlyIncome) < 43:
            print("Since your DTI is still less than 43%, it is possible you could be approved")
            return -4
        else:
            print("You must lower your DTI")
            return -5
    elif ~FEDTI_Pass:
        print("fedti too high")
        print("Better mortgage: "+ str(maxMortgage(CarPayment + CreditCardPayment + StudentLoanPayment)))
        return -6
    else:
        print("you pass!")
        return 1