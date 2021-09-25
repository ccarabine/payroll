import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('companypayroll')

employeedetail = SHEET.worksheet('employeedetail')
employeepayroll = SHEET.worksheet('employeepayroll')
employee_payroll_list = employeepayroll.get_all_values()

PAYROLL_WEEK = 34
HOL_PC = 0.1208
EMPLOYEES_NI_PC = 0.1392 
EMPLOYEES_NI_AMOUNT=156

EMPLOYERS_PENSION_PC =0.03
EMPLOYERS_NI_PC = 0.1
#main_menu_option = get_main_menu_option()

def get_payroll_week():
    """
    Get payroll week from user and validate
    Can only process and amend payroll for current week
  
    """
    while True:
        input_payroll_week=input("Enter Payroll Week (1-52) : ")
        if int(input_payroll_week) == PAYROLL_WEEK:
            if validate_data_int(input_payroll_week,1,52):
                return(input_payroll_week)
        else: 
            print (f'You can only enter /Amend payroll for the current week which is week {PAYROLL_WEEK}')
    

def get_employee_num():
    """
    Get employee number from user,validate to check that the employee is in the employee details list and retrieve details
    """ 
    while True:
        input_employee_num = input("Enter Employee number e.g. 100014  : ")
        print ("Finding Employment record")
        if validate_employee_num(input_employee_num):
            print ("Employment record retrieved")    
            return(input_employee_num)
                    
      
def get_employee_hours():
    """
    Get employees hours for week from user ( maximum 100 hours) and validate
    """
    while True:
        input_employee_hours=input("Enter number of hours worked : ")
        if validate_data_float(input_employee_hours,1,100):
            return(input_employee_hours)


def get_payroll_data(employee_entered_payroll_week,employee_num):
    """
    Get Employees details from spreadsheet and put into variables
    """
    employee_retrived_data = validate_employee_num(employee_num)
    employee_number =(employee_retrived_data[0])
    employee_surname =(employee_retrived_data[1])
    employee_firstname =(employee_retrived_data[2])
    employee_rate_of_pay=(employee_retrived_data[3])
    employee_pension=(employee_retrived_data[4])
    employee_hours = get_employee_hours()
   
    return (employee_entered_payroll_week,employee_number,employee_surname,employee_firstname,employee_rate_of_pay,employee_pension, employee_hours)
   
def calculate_employee_payslip_data(employee_entered_payroll_week,employee_num):
    """
    Calculates values for employees pay and employers contributions and puts values in a list
    """
    payroll_data=get_payroll_data(employee_entered_payroll_week,employee_num)
    week_no = (payroll_data[0]) 
    employee_number=(payroll_data[1]) 
    employee_surname=(payroll_data[2]) 
    employee_firstname=(payroll_data[3])
    
    employee_rate_of_pay=float(payroll_data[4])
    employee_pension=float(payroll_data[5]) 
    employee_hours=float(payroll_data[6]) 
    employee_basic_pay = round(employee_hours * employee_rate_of_pay,2)
    employee_holiday = round(employee_basic_pay * HOL_PC,2)
    employee_basic_hol = (employee_basic_pay + employee_holiday)
    if (employee_basic_pay + employee_holiday) < EMPLOYEES_NI_AMOUNT:
        employee_ni = 0
    else:
        employee_ni = round(((employee_basic_hol) - EMPLOYEES_NI_AMOUNT) * EMPLOYEES_NI_PC,2)
    employee_deducations = round(employee_ni + employee_pension,2)
    employee_pension= round(employee_pension * employee_basic_hol,2)
    employee_net_pay = round(employee_basic_hol - employee_ni - employee_pension,2)
    
    
    employers_ni = round(employee_basic_hol * EMPLOYERS_NI_PC,2)
    employers_pension = round(employee_basic_hol * EMPLOYERS_PENSION_PC,2)
    print(f'\n Employee : {employee_number} - {employee_firstname} {employee_surname}')
    print(f' Basic Pay : £{employee_basic_pay}')
    print(f' Holiday Pay : £{employee_holiday}')
    print(f' NI contribution: £{employee_ni}')
    print(f' Pension contribution: £{employee_pension}')
    print(f' Net Pay: £{employee_net_pay}')
    
    if yesorno("Are the amounts correct? "):
        print("Ready to upload into payroll spreadsheet")
        row_date=[]
        row_data= [week_no,employee_number,employee_surname,employee_firstname,employee_hours,employee_basic_pay,employee_holiday,employee_ni,employee_pension,employee_net_pay,employers_ni,employers_pension]
        update_worksheet(row_data,"employeepayroll")
        return (employee_basic_pay)
    else:
        print("Re enter details \n")
        calculate_employee_payslip_data()

#def search():
 #   employee_num=input("Employee num")
  #  search_value = employeedetail.findall(employee_num )
   # print(search_value)


def get_main_menu_option():
    """
    Get Main menu option input from user
    Run function related to input
    """
    while True:
        print("-------------- Main Menu -------------- ")
        print("1 Display payroll")
        print("2 Process / Amend payroll")
        print("3 Run payroll")
        print("4 Add / Amend employee details\n")
        print("Example:  1\n")

        main_menu_option_data = input("Please enter number option from the menu : ")
        if validate_data_int(main_menu_option_data,1,4):
            if main_menu_option_data == "1":
                get_display_payroll_option()
            if main_menu_option_data == "2":
                get_process_payroll_option()
            if main_menu_option_data == "3":
                get_run_payroll_option()
            if main_menu_option_data == "4":
                get_add_amend_employee_option()
                

def get_display_payroll_option():
    """
    Get display payroll option input from user
    Run function related to input
    """
    while True:
        print("-------------- Display Payroll -------------- ")
        print("1 All employees pay for week")
        print("2 Employee pay for week")
        print("3 Employers summary for week")
        print("4 Main menu\n")
        print("Example:  1\n")
        display_payroll_option_data = input("Please enter number option from the menu : ")
        if validate_data_int(display_payroll_option_data,1,4):
            if display_payroll_option_data == "1":
                get_allemployeepay_option()
            if display_payroll_option_data == "2":
                get_employeepay_option()
            if display_payroll_option_data == "3":
                get_employerssummaryay_option()
            if display_payroll_option_data == "4":
                get_main_menu_option()


def get_process_payroll_option():
    """
    Get process / Amend payroll option input from user
    Run function related to input
    """
    while True:
        print("-------------- Process / Amend Payroll -------------- ")
        print("1 Add Employees hours")
        print("2 Amend employees hours")
        print("3 Main menu\n")
        
        print("Example:  1\n")

        process_payroll_option_data = input("Please enter number option from the menu : ")
    
        if validate_data_int(process_payroll_option_data,1,3):
            if process_payroll_option_data == "1":
                calculate_employee_payslip_data()
                next_employee_to_process()
            if process_payroll_option_data == "2":
                amend_employees_hours()
            if process_payroll_option_data == "3":
                get_main_menu_option()
           
            
        return process_payroll_option_data


def get_add_amend_employee_option():
    """
    Get add / amend employee option input from user
    Run function related to input

    Future feature
    """
    while True:
        print("\n Feature in next update, returning to main menu \n")
        get_main_menu_option()
        
       
def validate_data_int(value,minvalue,maxvalue):
    """
    Inside the try, converts value to integer
    raise ValueError if strings cannot be converted into int or less than min or greater than max values
    """
    try:
       
        if int(value) < minvalue or int(value) > maxvalue:
            raise ValueError(
               f"Number between {minvalue} and {maxvalue} required, you typed {value}"
        )
    except ValueError as e:
        print(f"Invalid data, please try again.\n")
        return False

    return True

def validate_data_float(value,minvalue,maxvalue):
    """
    Inside the try, converts value to float
    raise ValueError if strings cannot be converted into float or less than min or greater than max value
    """
    try:
       
        if float(value) < minvalue or float(value) > maxvalue:
            raise ValueError(
               f"Number between {minvalue} and {maxvalue} required, you typed {value}"
        )
    except ValueError as e:
        print(f"Invalid data, please try again.\n")
        return False

    return True


def validate_employee_num(num):
    """
    Try: find employee number in employee detail sheet
        puts the row ref, rate of pay and pension into variables an returns rate of pay and pension
    except AttributeError if there isn't a value in the sheet then asks the user if they want to try again or return to the main menu
    """
    try:
        employee_row = employeedetail.find(num).row 
        
        values_list = employeedetail.row_values(employee_row)
        employee_number =employeedetail.cell(employee_row,1)
        employee_surname =employeedetail.cell(employee_row,2)
        employee_firstname =employeedetail.cell(employee_row,3)
        employee_rateofpay =employeedetail.cell(employee_row,4)
        employee_pension =employeedetail.cell(employee_row,5)
      
        return employee_number.value, employee_surname.value,employee_firstname.value,employee_rateofpay.value,employee_pension.value
    except AttributeError as e:
        print(f"\nInvalid employee number, please try again.\n")
        while True:
            if yesorno("Do you want to try again? type y or n :  "):
                break
            get_main_menu_option()

def check_data_in_payroll_sheet(week, employee_num):
    """
    Try: User requested to input payroll week and employee number. Checks to see if there is a record.  If there is it will delete the row
        and request user to put the details in again
        
    except IndexError if there isn't a value in the sheet then returns to the process/amend menu
    """
    employee_num_found = employeepayroll.findall(employee_num)
    week_found = employeepayroll.findall(week)
    em=[]
    for i in employee_num_found:
        em.append(i.row)
    wk=[]
    for i in week_found:
        wk.append(i.row)

    set1 = set(em)
    set2 = set(wk)
    intersect = list(set1 & set2)
    try: 
        print(intersect[0])
        print("already entered")
        if intersect[0] >= 1:
            print(f'A record has already been entered for employee number: {employee_num} in week {week} ')
            intersect=[]
            get_main_menu_option()
        else:
            return(week,employee_num)
    except IndexError as e:
        print(f' no record found do this - good to add a row continue')
        return(week,employee_num)
       
    
#orginal
def amend_employees_hourss():
    """
    Try: User requested to input payroll week and employee number. Checks to see if there is a record.  If there is it will delete the row
        and request user to put the details in again
        
    except IndexError if there isn't a value in the sheet then returns to the process/amend menu
    """
    try:
        week=get_payroll_week()
        num=get_employee_num()
    
        employee_num_found = employeepayroll.findall(num)
        week_found = employeepayroll.findall(week)
        em=[]
        for i in employee_num_found:
            em.append(i.row)
        wk=[]
        for i in week_found:
            wk.append(i.row)
        
        set1 = set(em)
        set2 = set(wk)
        intersect = list(set1 & set2)
        row_to_delete = intersect[0]
    
        employeepayroll.delete_rows(row_to_delete)
        print(f'Record deleted for {num} in week {week}. Please re-enter details')
        calculate_employee_payslip_data()

    except IndexError as e:
        print(f"\nNo payroll record found for {num} in week {week}, returning to main menu.\n")
        get_process_payroll_option()

def yesorno(question):
    """ 
     Function to take user input yes or no
     validate input
     Code used from https://gist.github.com/garrettdreyfus/8153571  
     """
    answer = input(f'{question}') 
    try:
        if answer[0] == 'y':
            return True
        elif answer[0] == 'n':
            return False
        else:
            print('Invalid entry')
            return yesorno(question)
    except Exception as error:
        print("Please enter valid entry")
        print(error)
        return yesorno()

def update_worksheet(data, worksheet):
    """
    Receives a list to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    Code taken from Love sandwiches project
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

def next_employee_to_process():
   """
   Requests user input if they would like to process another employees hours
   """ 
   while True:
            if yesorno("Would you like to process another employees hours? type y or n :  "):
                check_data_in_payroll_sheet()
                
            else:
                get_main_menu_option()




def main():
    """
    Run all program functions
    """
    week=get_payroll_week()
    num=get_employee_num()
    check_data_in_payroll_sheet(week,num)
    calculate_employee_payslip_data(week,num)
    next_employee_to_process()
#main_menu_option = get_main_menu_option()
#process_payroll=process_payroll()
#get_payroll_data=get_payroll_data()
    
#amend_employees_hours()    
print("Welcome to Payroll application")
main()
