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
    -1: error in given data
    -2: credit score too low: advise to pay off credit cards on time
    -3: LTV too high, might qualify with PMI: advise to either choose a larger down payment or purchase PMI (private mortgage insurance)
    -4: LTV too high: advise to choose a larger down payment
    -5: DTI too high: advise to choose a lower monthly mortgage rate
    -6: DTI too high: advise to transfer high interest loans to low interest credit cards (but not have too many credit cards either)
    -7: FEDTI too high: advise to choose a lower monthly mortgage rate
    
'''
def calculateApproval(CreditScore, GrossMonthlyIncome, CreditCardPayment, StudentLoanPayment, CarPayment, MonthlyMortgagePayment, AppraisedValue, DownPayment, LoanAmount):
    if LoanAmount + DownPayment != AppraisedValue or MonthlyMortgagePayment > LoanAmount:
        print("invalid data given: value constraints not met")
        return -1
    
    if CreditScore < 0 or GrossMonthlyIncome < 0 or CreditCardPayment < 0 or StudentLoanPayment < 0 or CarPayment < 0 or MonthlyMortgagePayment < 0 or AppraisedValue < 0 or DownPayment < 0 or LoanAmount < 0:
        print("invalid data given: data contains negative values")
        return -1

    Credit_Pass = CreditScore > 640
    LTV_Pass = ((LoanAmount/AppraisedValue)*100) < 80
    DTI_Pass = ((CarPayment+StudentLoanPayment+CreditCardPayment+MonthlyMortgagePayment)/GrossMonthlyIncome)*100 < 36 and MonthlyMortgagePayment / (MonthlyMortgagePayment + CreditCardPayment + CarPayment + StudentLoanPayment) * 100 <= 28
    FEDTI_Pass = (MonthlyMortgagePayment/GrossMonthlyIncome)*100 <= 28
    
    if ~Credit_Pass:
        print("Pay off debt etc etc")
        return -2
    elif ~LTV_Pass:
        print("you got a LTV problem")
        if LTVCalc(LoanAmount, AppraisedValue) < 95:
            print("max acctpable price: " + str(maxAcceptableValue(DownPayment)))
            print("min accptable down payment: " + str(minAcceptableDownpay(AppraisedValue)))
            return -3
        else:
            print("absolutly not")
            return -4
    elif ~DTI_Pass:
        print("you got a dti problm")
        if DTICalc(CarPayment + CreditCardPayment + StudentLoanPayment + MonthlyMortgagePayment, GrossMonthlyIncome) < 43:
            if MonthlyMortgagePayment / (MonthlyMortgagePayment + CreditCardPayment + CarPayment + StudentLoanPayment) * 100 > 28:
                print("Mortgage as percentage of total monthly debts is too high")
                print("Better mortgage: " + str(maxMortgage(CarPayment + CreditCardPayment + StudentLoanPayment)))
                return -5
            else:
                print("You must lower your DTI")
                return -6
        else:
            print("You must lower your DTI")
            return -6
    elif ~FEDTI_Pass:
        print("You must lower your FEDTI")
        print("Better mortgage: "+ str(maxMortgage(CarPayment + CreditCardPayment + StudentLoanPayment)))
        return -7
    else:
        print("you pass!")
        return 1