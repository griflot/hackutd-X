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
return tuples:
    (1): likely to be approved
    (-1): error in given data
    (-2): credit score too low: advise to pay off credit cards on time
    (-3, loweredAppraisedValue, raisedDownPayment): LTV too high, might qualify with PMI: advise to either choose a larger down payment or purchase PMI (private mortgage insurance)
    (-4, loweredAppraisedValue, raisedDownPayment): LTV too high: advise to choose a larger down payment
    (-5, lowerMortgage): DTI too high: advise to choose a lower monthly mortgage rate
    (-6): DTI too high: advise to transfer high interest loans to low interest credit cards (but not have too many credit cards either)
    (-7, lowerMortgage): FEDTI too high: advise to choose a lower monthly mortgage rate
'''
def calculateApproval(CreditScore, GrossMonthlyIncome, CreditCardPayment, StudentLoanPayment, CarPayment, MonthlyMortgagePayment, AppraisedValue, DownPayment, LoanAmount):
    if LoanAmount + DownPayment != AppraisedValue or MonthlyMortgagePayment > LoanAmount:
        print("invalid data given: value constraints not met")
        return (-1, None, None)
    
    if CreditScore < 0 or GrossMonthlyIncome < 0 or CreditCardPayment < 0 or StudentLoanPayment < 0 or CarPayment < 0 or MonthlyMortgagePayment < 0 or AppraisedValue < 0 or DownPayment < 0 or LoanAmount < 0:
        print("invalid data given: data contains negative values")
        return (-1, None, None)

    Credit_Pass = CreditScore > 640
    LTV_Pass = ((LoanAmount/AppraisedValue)*100) < 80
    DTI_Pass = ((CarPayment+StudentLoanPayment+CreditCardPayment+MonthlyMortgagePayment)/GrossMonthlyIncome)*100 < 36 and MonthlyMortgagePayment / (MonthlyMortgagePayment + CreditCardPayment + CarPayment + StudentLoanPayment) * 100 <= 28
    FEDTI_Pass = (MonthlyMortgagePayment/GrossMonthlyIncome)*100 <= 28
    
    if ~Credit_Pass:
        print("Pay off debt etc etc")
        return (-2, None, None)
    elif ~LTV_Pass:
        print("you got a LTV problem")
        loweredAppraisedValue = maxAcceptableValue(DownPayment)
        raisedDownPayment = minAcceptableDownpay(AppraisedValue)
        print("max acctpable price: " + str(loweredAppraisedValue))
        print("min accptable down payment: " + str(raisedDownPayment))
        LTV = LTVCalc(LoanAmount, AppraisedValue)
        if LTV >= 80 and LTV <= 95:
            return (-3, loweredAppraisedValue, raisedDownPayment)
        else:
            return (-4, loweredAppraisedValue, raisedDownPayment)
    elif ~DTI_Pass:
        print("you got a dti problm")
        if DTICalc(CarPayment + CreditCardPayment + StudentLoanPayment + MonthlyMortgagePayment, GrossMonthlyIncome) < 43:
            if MonthlyMortgagePayment / (MonthlyMortgagePayment + CreditCardPayment + CarPayment + StudentLoanPayment) * 100 > 28:
                print("Mortgage as percentage of total monthly debts is too high")
                lowerMortgage = maxMortgage(CarPayment + CreditCardPayment + StudentLoanPayment)
                print("Better mortgage: " + str(lowerMortgage))
                return (-5, lowerMortgage, None)
            else:
                print("You must lower your DTI")
                return (-6, None, None)
        else:
            print("You must lower your DTI")
            return (-6, None, None)
    elif ~FEDTI_Pass:
        print("You must lower your FEDTI")
        lowerMortgage = maxMortgage(CarPayment + CreditCardPayment + StudentLoanPayment)
        print("Better mortgage: "+ str(lowerMortgage))
        return (-7, lowerMortgage, None)
    else:
        print("you pass!")
        return (1, None, None)