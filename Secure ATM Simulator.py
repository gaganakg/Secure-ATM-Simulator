import mysql.connector
import re
import twilio.rest 
import math, random
from datetime import datetime
import pandas as pd
import os
import time
from decimal import Decimal
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from colorama import init, Back, Fore
from rich.console import Console



number_twilio = ''   #replace the empty string with twilio ph no. in string format
account_sid = '' #replace the empty string with associated account sid in string format
auth_token = '' #replace the empty string with associated auth token in string format

phone = []
client = twilio.rest.Client(account_sid, auth_token)

init(autoreset=True)
console = Console()

def clear_screen():
    if os.name == 'nt':
        os.system('cls')

def print_with_background(message, background_color):
    print(f"{background_color}{Fore.WHITE}{message}{Back.RESET}{Fore.RESET}")

def print_menu(menu, background_color):
    print_with_background(menu, background_color)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gagana",
    database="ATM",
    autocommit = True
)


mycursor = mydb.cursor()

def clear():
    os.system("cls")


class ATM:
    def _init_(self, VCN, PHN, PIN):
        self.VCN = VCN
        self.PHN = PHN
        self.PIN = PIN

def clear():
    os.system("cls")

def menu1():
    menu = """
        1. Login
        2. Register
        3. Exit
    """
    print_menu(menu, Back.BLUE)

def menu2():
    menu = """
        1. Withdraw
        2. Deposit
        3. Transaction history
        4. Check balance
        5. Change PIN
        6. Account-to-Account Transfer
        7. Exit
    """
    print_menu(menu,Back.BLUE)

def withdraw(VCN):
    limit = 4
    lim_amt=3
    flag=0
    while limit > 0:
        if PIN_check(VCN):
            
            while lim_amt>0 and flag==0:
                value = input("\nEnter Amount (In Hundreds only): ")
                if not value.isdigit():
                    print("\nPlease enter a valid amount")
                    lim_amt=lim_amt-1
                elif value.isdigit() and int(value)%100!=0:
                    print()
                    print("Please enter a value which is divisible by 100")
                    lim_amt=lim_amt-1
                else:
                    value=int(value)
                    flag=1
                    break
                    
            if flag == 1:
                date_time = datetime.now().strftime("%d%m%Y%H%M%S")
                id= str(VCN)+date_time
                mycursor.execute(f"SELECT balance FROM users WHERE VCN={VCN}")
                amount = int(mycursor.fetchone()[0])
                    
                if (amount - value)<0:
                    print("\n Insufficient Balance, please check your balance and try again.")
                    break
                else:
                    mycursor.execute(f'''UPDATE users SET balance = {int(amount-value)} WHERE VCN = {VCN}''')
                    mycursor.execute("insert into transactions (VCN, transaction_id, transaction_amount,  Type) values(%s, %s, %s,  %s)", (VCN, id, value,  "Withdraw", ))
                    
                    print("\n The amount has been processed")
                    
                    
                    
                    
                    
                    messages = client.messages.create(
                        from_=number_twilio,
                        body=f'There was a withdraw of amount {value}Rs. from your account. Your current account balance is {amount-value}Rs.',
                        to= str(phone[0])
                    )
                
                break
            else:
                print("\nPlease try again later")
                return
            
        else:
            print(f"Incorrect PIN. {limit - 1} attempts remaining.")
        limit -= 1
    if limit == 0:
        print("Maximum PIN attempts reached. Exiting.")
        return
    
def deposit(VCN):
    limit = 4
    lim_amt=3
    flag=0
    while limit > 0:
        if PIN_check(VCN):
            
            while lim_amt>0 and flag==0:
                value = input("\nEnter Amount (In Hundreds only): ")
                if not value.isdigit():
                    print("\nPlease enter a valid amount")
                    lim_amt=lim_amt-1
                elif value.isdigit() and int(value)%100!=0:
                    print()
                    print("Please enter a value which is divisible by 100")
                    lim_amt=lim_amt-1
                else:
                    value=int(value)
                    flag=1
                    break
            
            if(flag==1):
                date_time = datetime.now().strftime("%d%m%Y%H%M%S")
                id= str(VCN)+date_time
                mycursor.execute(f"SELECT balance FROM users WHERE VCN={VCN}")
                amount = int(mycursor.fetchone()[0])
                    
                
                mycursor.execute(f'''UPDATE users SET balance = {int(amount+value)} WHERE VCN = {VCN}''')
                mycursor.execute("insert into transactions (VCN, transaction_id, transaction_amount,  Type) values(%s, %s, %s,  %s)", (VCN, id, value,  "Deposit", ))
                
                
                    
                    
                messages = client.messages.create(
                    from_=number_twilio,
                    body=f'There was a deposit of amount {value}Rs to your account. Your current account balance is {amount+value}Rs.',
                    to= str(phone[0])
                )
                    
                print("\n The amount has been processed")
                break
            else:
                print("\nPlease try again later")
                return
            
        else:
            print(f"Incorrect PIN. {limit - 1} attempts remaining.")
        limit = limit-1
    if limit == 0:
        print("Maximum PIN attempts reached. Exiting.")
        return
    
    
def balance(VCN):
    limit = 4
    while limit > 0:
        if PIN_check(VCN):
        
            mycursor.execute(f"SELECT balance FROM users WHERE VCN={VCN}")
            amount = int(mycursor.fetchone()[0])
                
            print(f"Your account balance is {amount}")
            
            
            time.sleep(1)
                
            messages = client.messages.create(
                from_= number_twilio,
                body=f'Your current account balance is {amount}Rs.',
                to= str(phone[0])
            )
            
            break
            
        else:
            print(f"Incorrect PIN. {limit - 1} attempts remaining.")
        limit -= 1
    if limit == 0:
        print("Maximum PIN attempts reached. Exiting.")
        return

def transaction_details(VCN):
    limit = 4
    while limit > 0:
        if PIN_check(VCN):
            query = f"select * from transactions where VCN = {VCN}"
        
            mycursor.execute(query)
            rows = mycursor.fetchall()
            columns = [desc[0] for desc in mycursor.description]
            df = pd.DataFrame(rows, columns=columns)
            print()
            print(df)
            
            message = "Your last 5 transactions: "
            
            for index, row in df.iterrows():
                message += f"transaction id: {row['TRANSACTION_ID']}, amount: {row['TRANSACTION_AMOUNT']}, transaction type: {row['TYPE']}"
            
                if index==4:
                    break
            
            client.messages.create(
                        from_=number_twilio,
                        body=message,
                        to= str(phone[0])
                    )
            break
            
        else:
            print(f"Incorrect PIN. {limit - 1} attempts remaining.")
        limit -= 1
    if limit == 0:
        print("Maximum PIN attempts reached. Exiting.")
        return


def transfer(VCN):
    VCN2 = input("Enter VCN: ")
    limit = 4
    lim_amt=3
    flag = 0
    if VCN_match(VCN2):
        while limit > 0:
            if PIN_check(VCN):
                while lim_amt>0 and flag==0:
                    value = input("\nEnter Amount (In Hundreds only): ")
                    if not value.isdigit():
                        print("\nPlease enter a valid amount")
                        lim_amt=lim_amt-1
                    elif value.isdigit() and int(value)%100!=0:
                        print()
                        print("Please enter a value which is divisible by 100")
                        lim_amt=lim_amt-1
                    else:
                        value=int(value)
                        flag=1
                        break
                if(flag==1):
                    date_time = datetime.now().strftime("%d%m%Y%H%M%S")
                    id= str(VCN)+date_time
                    mycursor.execute(f"SELECT balance FROM users WHERE VCN={VCN}")
                    amount = int(mycursor.fetchone()[0])

                    mycursor.execute(f"SELECT balance FROM users WHERE VCN={VCN2}")
                    amount2 = int(mycursor.fetchone()[0])
                    
                    if (amount - value)<0:
                        print("\n Insufficient Balance, please check your balance and try again.")
                        break
                    else:
                        mycursor.execute(f'''UPDATE users SET balance = {int(amount-value)} WHERE VCN = {VCN}''')
                        mycursor.execute(f'''UPDATE users SET balance = {int(amount2+value)} WHERE VCN = {VCN2}''')
                        mycursor.execute("insert into transactions (VCN, transaction_id, transaction_amount, VCN2, Type) values(%s, %s, %s, %s, %s)", (VCN, int(id), value,  VCN2,"Sent", ))
                        mycursor.execute("insert into transactions (VCN, transaction_id, transaction_amount, VCN2, Type) values(%s, %s, %s, %s, %s)", (VCN2, int(id+"1"), value,  VCN,"recieved", ))
                        print("\n The amount has been processed")
                        
                        
                        mycursor.execute(f"SELECT PHN FROM users WHERE VCN={VCN2}")
                        phone2 = str(mycursor.fetchone()[0])
                        if "+91" not in phone2:
                            phone2 = "+91" + phone2
                        
                    
                        messages = client.messages.create(
                            from_=number_twilio,
                            body=f'An amount of {value}Rs. Was transferred to account number {VCN2}. Your current account balance is {amount2+value}',
                            to= str(phone2)
                        )
                        
                    
                    
                        messages = client.messages.create(
                            from_=number_twilio,
                            body=f'An amount of {value}Rs. Was transferred from account number {VCN}. Your current account balance is {amount-value}',
                            to= str(phone[0])
                        )
                        break
                else:
                    print("\nPlease try again later")
                    return  
            else:
                print(f"Incorrect PIN. {limit - 1} attempts remaining.")
            limit -= 1
        if limit == 0:
            print("Maximum PIN attempts reached. Exiting.")
            return
    else:
        print("VCN not found. Exiting.")
        return





def validate_re_ph(phone_number):
    expr = r'^(0|91)?[6-9][0-9]{9}$'
    if not re.match(expr, phone_number):
        print("\nPhone number is invalid")
        return 0

    mycursor.execute("SELECT COUNT(*) FROM users WHERE PHN = %s", (phone_number,))
    result = mycursor.fetchone()
    count = result[0] if result else 0
    
    if int(count) > 0:
        print("\nAccount with the entered phone number already exists.")
        return 0
    return 1

def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def send_verify_otp(ph, VCN_exist):
    otp = generateOTP()
    if not VCN_exist:
        limit_otp_send = 5

    ask_user = 1

    while limit_otp_send > 0 and ask_user:
        limit_otp_match = 5
        if len(ph) == 10:
            ph = "+91" + ph
         
        
        

        message = client.messages.create(
            from_=number_twilio,
            body='ATM simulator OTP: ' + otp,
            to=ph
        )
        print("\nOTP sent to your mobile number")
        input_otp = input("\nEnter OTP sent:")

        while input_otp != otp and limit_otp_match > 1:
            input_otp = input("\nRe-enter OTP sent: ")
            limit_otp_match = limit_otp_match - 1

        if limit_otp_match <= 1:
            print("\t1.Resend OTP")
            print("\t2. Later")
            ask_user = input("Select an option ")
            if ask_user == "1":
                pass
            elif ask_user == "2":
                ask_user = 0
                if VCN_exist:
                    limit_left = limit_otp_send
            else:
                print("\t1.Invalid option. Try again later")
        else:
            print("\nOTP successfully verified!")
            return 1
        limit_otp_send = limit_otp_send - 1

    if limit_otp_send <= 0:
        print("\tTry again later after 24 hours")
    elif ask_user == 0:
        print("\tTry again later")

    return 0

def set_the_pin(vcn, ph, vcn_exist):
    temp_limit = 3

    input_PIN = input("\nEnter a 4 digit PIN:")

    if len(input_PIN) == 4 and input_PIN.isdigit():
        while temp_limit > 0:
            c_input_PIN = input("\nRe-enter PIN to confirm:")
            if c_input_PIN != input_PIN:
                print("\nThe PINs do not match")
                temp_limit = temp_limit - 1
            else:
                if vcn_exist == 0:  # Check if it's a new registration
                    sql = "insert into users (VCN, PHN, PIN, BALANCE) values(%s, %s, %s, %s)"
                    val = (vcn, ph, c_input_PIN, 1)
                    messages = client.messages.create(
                        from_=number_twilio,
                        body=f'The pin to your account has been set!',
                        to= str(phone[0])
                    )
                else:  # It's a PIN change, update the existing record
                    sql = "UPDATE users SET PIN = %s WHERE VCN = %s"
                    val = (c_input_PIN, vcn)
                    
                
                
                    messages = client.messages.create(
                        from_=number_twilio,
                        body=f'New pin has been set!',
                        to= str(phone[0])
                    )
                mycursor.execute(sql, val)
                
                print("\nYou've successfully set your PIN")
                #print("\nPlease login to continue")
                return 3
    else:
        print("\nEnter a valid PIN")
        return 2
    return 1

def login():
    VCN = input("Enter VCN: ")
    limit = 4
    if VCN_match(VCN):
        while limit > 0:
            if PIN_check(VCN):
                
                break
            else:
                print(f"Incorrect PIN. {limit - 1} attempts remaining.")
            limit -= 1
        if limit == 0:
            print("Maximum PIN attempts reached. Exiting.")
            return
    else:
        print("VCN not found. Exiting.")
        return
    
    mycursor.execute(f"SELECT PHN FROM users WHERE VCN={VCN}")
    phone1 = str(mycursor.fetchone()[0])
    if "+91" not in phone1:
        phone1 = "+91" + phone1
    phone.clear()
    phone.append(phone1)
    while True:
        menu2()
        ch = input("\nEnter choice: ")
        clear()
        if not ch.isdigit() or (int(ch)<0 or int(ch)>7):
            chances=2
            flag=0
            while chances>0 and flag==0:
                print("\nPlease enter a valid choice")
                ch = input("\nEnter choice: ")
                if ch.isdigit() and (int(ch)>=1 and int(ch)<=7):
                    flag=1
                chances=chances-1
            if chances==0 and flag==0:
                print("\nPlease try again later")
                return
            
        if ch == "1":
            print("\nWithdraw")
            print()
            withdraw(VCN)
            
            
        elif ch == "2":
            print("\nDeposit")
            print()
            deposit(VCN)
            
            
            
        elif ch == "3":
            print("\nTransaction History")
            print()
            transaction_details(VCN)
            print()
            
            
        elif ch == "4":
            print("\nCheck balance")
            balance(VCN)
            
            
        elif ch == "5":
            # Call the set_the_pin function to change the PIN
            set_the_pin(VCN, None, 1)

            
        elif ch=="6":
            print("\nTransfer")
            print()
            transfer(VCN)
            
            
        elif ch=="7":
            print("\nThank you for banking with us!")
            break
        else:
            print("\nInvalid option")
                
    input()
    clear()

def register():
    ph = input("Enter phone number: ")
    trials = 10
    pin_enter_limit = 3
    PIN = ""
    while trials > 0 and (not validate_re_ph(ph)):
        ph = input("\nEnter phone number: ")
        trials -= 1
    if trials <= 0:
        print("\nTry again later")
        return
    try:
        if send_verify_otp(ph, 0):
            mycursor.execute("SELECT VCN FROM users ORDER BY VCN DESC LIMIT 1")
            result = mycursor.fetchone()
            y = 0
            if result is not None:
                y = result[0]
            vcn = int(y) + 1
            print("\nYou can set the PIN now!")
            phone1 = str(ph)
            if "+91" not in phone1:
                phone1 = "+91"+phone1
            phone.clear()
            phone.append(phone1)
            
            
            VCN_PIN_status = set_the_pin(vcn, ph, 0)
            ask_user = 1
            
            while (ask_user == 1) and (VCN_PIN_status == 1 or VCN_PIN_status == 2) and pin_enter_limit > 1:
                print("\n\t1.Set PIN")
                print("\t2.Exit")
                ask_user = input("\nSelect an option ")
                if ask_user.isdigit():
                    ask_user=int(ask_user)
                    if ask_user == 1:
                        VCN_PIN_status = set_the_pin(vcn, ph, 0)
                        pin_enter_limit = pin_enter_limit - 1

                    elif ask_user == 2:
                        print("\nPlease try again later")
                        return
                    else:
                        print("\nInvalid option. Please try again later")
                        return
                else:
                    print("\nInvalid option. Please try again later")
                    return
            if pin_enter_limit == 1:
                print("\nAccount registration unsuccessful. Please try again later")
                return

            messages = client.messages.create(
                    from_=number_twilio,
                    body=f'Congratulations! You have successfully created an account with account number {vcn}. Happy Banking!',
                    to= str(phone[0])
                )
    except Exception as e:
        #print(e)
        input()
        if "send_verify_otp" in str(e):
            print("\nPhone number is not verified by Twilio (dev stage)")
            
def PIN_check(VCN):
    entered_PIN = input("Enter the PIN: ")
    mycursor.execute("SELECT PIN FROM users WHERE VCN = %s", (VCN,))
    result = mycursor.fetchone()
    if result:
        stored_PIN = result[0]
        if entered_PIN == stored_PIN:
            return True
    return False

def VCN_match(VCN):
    mycursor.execute("SELECT COUNT(*) FROM users WHERE VCN = %s", (VCN,))
    result = mycursor.fetchone()
    count = result[0] if result else 0
    if count > 0:
        return True
    return False

def pin_reset(VCN):
    if VCN_match(VCN):
        ph = input("Enter your phone number: ")
        if validate_re_ph(ph):
            if send_verify_otp(ph, 1):
                new_pin = input("Enter a new 4-digit PIN: ")
                if len(new_pin) == 4 and new_pin.isdigit():
                    c_new_pin = input("Re-enter the new PIN to confirm: ")
                    if new_pin == c_new_pin:
                        mycursor.execute("UPDATE users SET PIN = %s WHERE VCN = %s", (new_pin, VCN))
                        
                        print("PIN reset successful")
                    else:
                        print("The new PINs do not match. PIN reset failed")
                else:
                    print("Enter a valid 4-digit PIN")
            else:
                print("OTP verification failed. PIN reset failed")
        else:
            print("Invalid phone number. PIN reset failed")
    else:
        print("VCN not found. PIN reset failed")

    

while True:
    menu1()
    ch = input("\nEnter choice: ")
    if not ch.isdigit() or (int(ch)<0 or int(ch)>3):
        chances=2
        flag=0
        while chances>0 and flag==0:
            print("\nPlease enter a valid choice")
            ch = input("\nEnter choice: ")
            if ch.isdigit() and (int(ch)>=1 and int(ch)<=3):
                flag=1
            chances=chances-1
        if chances==0 and flag==0:
            print("\nPlease try again later")
            break
    if ch == "1":
        login()
        clear()
    elif ch == "2":
        register()
        clear()
    else:
        break
    
        
        
