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
    1: passed loan approval
    -1: credit score too low
    -2: LTV too high, possible fix
    -3: LTV too high
    -4: DTI too high, FEDTI too high
    -5: DTI too high
    -6: FEDTI too high
    -7: FEDT
    -8: error in given data
'''
def calculateApproval(CreditScore, GrossMonthlyIncome, CreditCardPayment, StudentLoanPayment, CarPayment, MonthlyMortgagePayment, AppraisedValue, DownPayment, LoanAmount):
    if LoanAmount + DownPayment != AppraisedValue or MonthlyMortgagePayment > LoanAmount:
        print("invalid data given: value constraints not met")
        return -8
    
    if CreditScore < 0 or GrossMonthlyIncome < 0 or CreditCardPayment < 0 or StudentLoanPayment < 0 or CarPayment < 0 or MonthlyMortgagePayment < 0 or AppraisedValue < 0 or DownPayment < 0 or LoanAmount < 0:
        print("invalid data given: data contains negative values")
        return -8

    Credit_Pass = CreditScore > 640
    LTV_Pass = ((LoanAmount/AppraisedValue)*100) < 80
    DTI_Pass = ((CarPayment+MonthlyMortgagePayment+CreditCardPayment)/GrossMonthlyIncome)*100 < 36
    FEDTI_Pass = (MonthlyMortgagePayment/GrossMonthlyIncome)*100 <= 28
    
    if ~Credit_Pass:
        print("Pay off debt etc etc")
        return -1
    elif ~LTV_Pass:
        print("you got a LTV problem")
        if LTVCalc(LoanAmount, AppraisedValue) <95:
            print("max acctpable price: " + str(maxAcceptableValue(DownPayment)))
            print("min accptable down payment: " + str(minAcceptableDownpay(AppraisedValue)))
            return -2
        else:
            print("absolutly not")
            return -3
    elif ~DTI_Pass:
        print("you got a dti problm")
        if DTICalc(CarPayment + CreditCardPayment + StudentLoanPayment +MonthlyMortgagePayment, GrossMonthlyIncome) >36:
            if ~FEDTI_Pass:
                print("fedti too high")
                print("Better mortgage: "+ str(maxMortgage(CarPayment + CreditCardPayment + StudentLoanPayment)))
                return -4
            else:
                print("spend less, get better loans")
                return -5
        else:
            print("literally no, hello??")
            return -6
    elif ~FEDTI_Pass:
        print("fedti too high")
        print("Better mortgage: "+ str(maxMortgage(CarPayment + CreditCardPayment + StudentLoanPayment)))
        return -7
    else:
        print("you pass!")
        return 1