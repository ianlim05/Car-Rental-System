
import datetime
import os

current_directory = os.getcwd()

class RentalTransaction:
    def __init__(self, car_registration_number, customer_id, rental_date, return_date, total_rental):
        self.car_registration_number = car_registration_number
        self.customer_id = customer_id
        self.rental_date = rental_date
        self.return_date = return_date
        self.total_rental = total_rental

def view_monthly_revenue(year, month):
    rental_transactions_in_month = []
    with open('car_rental.txt', 'r') as file:
        for line in file:
            transaction_data = line.strip().split(', ')
            transaction_info = {}
            for item in transaction_data:
                key, value = item.split(': ')
                transaction_info[key.strip()] = value.strip()

            # Parse dates from string to datetime
            rental_date = datetime.datetime.strptime(transaction_info['Rental Date'], "%d %B %Y").date()
            return_date = datetime.datetime.strptime(transaction_info['Return Date'], "%d %B %Y").date()

            # Check if the transaction falls within the specified month
            if rental_date.year == year and rental_date.month == month:
                rental_transaction = RentalTransaction(transaction_info['Car Registration Number'],
                                                       transaction_info['Customer ID'],
                                                       rental_date,
                                                       return_date,
                                                       float(transaction_info['Total Rental'].replace('RM', '')))
                rental_transactions_in_month.append(rental_transaction)

    if not rental_transactions_in_month:
        print("No rental transactions found for the specified month.")
        return

    total_revenue = sum(transaction.total_rental for transaction in rental_transactions_in_month)

    print("Monthly Revenue Report for {}/{}:".format(month, year))
    print("Total Revenue: RM{:.2f}".format(total_revenue))
    
def login(username_input, password_input):
    attempts = 0  # Initialize the attempts counter
    
    while attempts < 3:  # Continue the loop until three attempts are reached
        username = username_input  # Assign the input username to a local variable
        password = password_input  # Assign the input password to a local variable

        # Helper function to check login in a given file
        def check_login(file_name):
            try:
                with open(file_name, 'r') as file:
                    for line_num, line in enumerate(file, start=1):
                        if f"username: {username}" in line:
                            data = line.strip().split(', ')
                            current_user = {}
                            for info in data:
                                try:
                                    key, value = info.split(': ')
                                    current_user[key.strip()] = value.strip()
                                except ValueError:
                                    print(f"Skipping line {line_num} with invalid data format in file '{file_name}'")
                                    continue
                            if current_user.get('password') == password:
                                return f"Login successful. Welcome {current_user.get('role')}!"
            except FileNotFoundError:
                print(f"Error: The file '{file_name}' was not found.")
            except ValueError as ve:
                print(f"Error processing file '{file_name}': {ve}")
            return None

        # Check for login in different roles
        result = check_login('manager.txt') or check_login('customer_staff.txt') or check_login('car_service_staff.txt')
        
        if result:
            return result

        attempts += 1  # Increment the attempts counter
        print(f"Error: Invalid username or password. You have {3 - attempts} attempt(s) remaining.")
        if attempts < 3:
            username_input = input("Username: ")  # Prompt for username again
            password_input = input("Password: ")  # Prompt for password again

    return "Maximum login attempts reached. Please try again later."

# Get username and password from user input
username_input = input("Username: ")
password_input = input("Password: ")

# Call the login function with the provided arguments
currentuser = login(username_input, password_input)

# Check the login result and print the appropriate message
print(currentuser)





def roleoptions():
    print('''
ROLES OPTIONS
1.Customer Service Staff 
2.Car Service Staff
3.Manager  ''')
current_date = datetime.datetime.now().strftime("%d-%m-%Y")
#register newstaff
def register(staffid, password, role, name,  current_date):
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")
    
    if role == 'Customer Service Staff':
        with open('customer_staff.txt', 'a') as file:
            file.write(f"username: {staffid}, name: {name}, password: {password}, role: {role}, registerdate: {current_date}\n")
   
    elif role == 'Car Service Staff':
        with open('car_service_staff.txt', 'a') as file:
            file.write(f"username: {staffid}, name: {name}, password: {password}, role: {role}, registerdate: {current_date}\n")
            
    elif role == 'Manager':
        with open('manager.txt', 'a') as file:
            file.write(f"username: {staffid}, name: {name}, password: {password}, role: {role}, registerdate: {current_date}\n")


#a menu for manager          
def managermenu():
        print('''
MENU
1. REGISTER NEW STAFF
2. UPDATE STAFF DETAILS
3. DELETE STAFF RECORD
4. SET RENTING RATES
5. UPDATE RENTING RATES
6. VIEW MONTHLY REVENUE REPORT
7. UPDATE OWN PROFILE''')
 #login page

def update_text_file(file_path, data):
     with open(file_path, 'w') as file:
        for item in data:
            file.write(f"username: {item['username']}, name: {item['name']}, password: {item['password']}, role: {item['role']}, register date: {item['registerdate']}\n")
 
def updatemanagerinfoname(username, new_name):
    updated_manager_list = []  # Create an empty list to store updated manager information
    with open('manager.txt', 'r') as file:
        for line in file:
            if f"username: {username}" in line:
                data = line.strip().split(', ')
                updated_info = {}
                for info in data:
                    key, value = info.split(': ')
                    if key.strip() == 'name':
                        updated_info[key.strip()] = new_name  # Update the name
                    else:
                        updated_info[key.strip()] = value.strip()
                updated_manager_list.append(updated_info)
            else:
                updated_manager_list.append(line.strip())

    # Write the updated manager information back to the file
    with open('manager.txt', 'w') as file:
        for item in updated_manager_list:
            if isinstance(item, dict):
                file.write(', '.join([f"{key}: {value}" for key, value in item.items()]) + '\n')
            else:
                file.write(item + '\n')

def update_staff1_username(role, update_username, new_username):
    # Define the file path based on the role
    file_path ='customer_staff.txt'
    
    # Read data from the text file
    updated_data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            staff_info = line.strip().split(', ')
            staff_dict = {}
            for info in staff_info:
                key, value = info.split(': ')
                staff_dict[key.strip()] = value.strip()
            updated_data.append(staff_dict)
    
    # Update the username in the data
    for staff_data in updated_data:
        if staff_data['username'] == update_username:
            staff_data['username'] = new_username
            break
    
    # Write the updated data back to the text file
    with open(file_path, 'w') as file:
        for staff_data in updated_data:
            file.write(', '.join([f"{key}: {value}" for key, value in staff_data.items()]) + '\n')

        

def update_staff_1_name(role, update_username, new_name):
        # Define the file path based on the role
    file_path = "customer_staff.txt"

           # Read data from the text file
    updated_data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            staff_info = line.strip().split(', ')
            staff_dict = {}
            for info in staff_info:
                key, value = info.split(': ')
                staff_dict[key.strip()] = value.strip()
            updated_data.append(staff_dict)

       # Update the name in the data
    for staff_data in updated_data:
        if staff_data['username'] == update_username:
            staff_data['name'] = new_name
            break

                               # Write the updated data back to the text file
    with open(file_path, 'w') as file:
        for staff_data in updated_data:
            file.write(', '.join([f"{key}: {value}" for key, value in staff_data.items()]) + '\n')




def update_customer_staff_1_password(role, update_username, new_password):
    # Define the file path based on the role
    file_path = "customer_staff.txt"

    # Read data from the text file
    updated_data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            staff_info = line.strip().split(', ')
            staff_dict = {}
            for info in staff_info:
                key, value = info.split(': ')
                staff_dict[key.strip()] = value.strip()
            updated_data.append(staff_dict)

       # Update the password in the data
        for staff_data in updated_data:
            if staff_data['username'] == update_username:
                staff_data['password'] = new_password
                break

       # Write the updated data back to the text file
        with open(file_path, 'w') as file:
            for staff_data in updated_data:
                file.write(', '.join([f"{key}: {value}" for key, value in staff_data.items()]) + '\n')
                
def update_manager_username(role, update_username, new_username):
    # Define the file path based on the role
    file_path ='manager.txt'
    
    # Read data from the text file
    updated_data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            staff_info = line.strip().split(', ')
            staff_dict = {}
            for info in staff_info:
                key, value = info.split(': ')
                staff_dict[key.strip()] = value.strip()
            updated_data.append(staff_dict)
    
    # Update the username in the data
    for staff_data in updated_data:
        if staff_data['username'] == update_username:
            staff_data['username'] = new_username
            break
    
    # Write the updated data back to the text file
    with open(file_path, 'w') as file:
        for staff_data in updated_data:
            file.write(', '.join([f"{key}: {value}" for key, value in staff_data.items()]) + '\n')

                                         
                                
def update_manager_name(role, update_username, new_name):
# Define the file path based on the role
    file_path = "manager.txt"
    
       # Read data from the text file
    updated_data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            staff_info = line.strip().split(', ')
            staff_dict = {}
            for info in staff_info:
                key, value = info.split(': ')
                staff_dict[key.strip()] = value.strip()
            updated_data.append(staff_dict)
    
           # Update the name in the data
    for staff_data in updated_data:
        if staff_data['username'] == update_username:
            staff_data['name'] = new_name
            break
    
       # Write the updated data back to the text file
    with open(file_path, 'w') as file:
        for staff_data in updated_data:
            file.write(', '.join([f"{key}: {value}" for key, value in staff_data.items()]) + '\n')
    
    


def update_manager_password(role, update_username, new_password):
    # Define the file path based on the role
    file_path = "manager.txt"
    
           # Read data from the text file
    updated_data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            staff_info = line.strip().split(', ')
            staff_dict = {}
            for info in staff_info:
                key, value = info.split(': ')
                staff_dict[key.strip()] = value.strip()
            updated_data.append(staff_dict)
    
           # Update the password in the data
        for staff_data in updated_data:
            if staff_data['username'] == update_username:
                staff_data['password'] = new_password
                break
    
       # Write the updated data back to the text file
        with open(file_path, 'w') as file:
            for staff_data in updated_data:
                file.write(', '.join([f"{key}: {value}" for key, value in staff_data.items()]) + '\n')
                
def update_carstaff_username(role, update_username, new_username):
    # Define the file path based on the role
    file_path ='car_service_staff.txt'
    
    # Read data from the text file
    updated_data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            staff_info = line.strip().split(', ')
            staff_dict = {}
            for info in staff_info:
                key, value = info.split(': ')
                staff_dict[key.strip()] = value.strip()
            updated_data.append(staff_dict)
    
    # Update the username in the data
    for staff_data in updated_data:
        if staff_data['username'] == update_username:
            staff_data['username'] = new_username
            break
    
    # Write the updated data back to the text file
    with open(file_path, 'w') as file:
        for staff_data in updated_data:
            file.write(', '.join([f"{key}: {value}" for key, value in staff_data.items()]) + '\n')

        

def update_carstaff_name(role, update_username, new_name):
        # Define the file path based on the role
    file_path = 'car_service_staff.txt'

    # Read data from the text file
    updated_data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            staff_info = line.strip().split(', ')
            staff_dict = {}
            for info in staff_info:
                key, value = info.split(': ')
                staff_dict[key.strip()] = value.strip()
            updated_data.append(staff_dict)

                # Update the name in the data
    for staff_data in updated_data:
        if staff_data['username'] == update_username:
            staff_data['name'] = new_name
            break

                # Write the updated data back to the text file
    with open(file_path, 'w') as file:
        for staff_data in updated_data:
            file.write(', '.join([f"{key}: {value}" for key, value in staff_data.items()]) + '\n')




def update_carstaff_password(role, update_username, new_password):
    # Define the file path based on the role
    file_path = 'car_service_staff.txt'

    # Read data from the text file
    updated_data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            staff_info = line.strip().split(', ')
            staff_dict = {}
            for info in staff_info:
                key, value = info.split(': ')
                staff_dict[key.strip()] = value.strip()
            updated_data.append(staff_dict)

        # Update the password in the data
        for staff_data in updated_data:
            if staff_data['username'] == update_username:
                staff_data['password'] = new_password
                break

                        # Write the updated data back to the text file
        with open(file_path, 'w') as file:
            for staff_data in updated_data:
                file.write(', '.join([f"{key}: {value}" for key, value in staff_data.items()]) + '\n')

def print_customer_staff_1_data():
    with open('customer_staff.txt', 'r') as file:
        print()
        print("Customer Service Staff List:")
        print()
        lines = file.readlines()
        for line in lines:
            if line.strip():  # Check if the line is not empty
                data = line.strip().split(', ')
                for item in data:
                    key, value = item.split(': ')
                    print(f"{key}: {value}")
                print()
                    

def delete_staff1_info(username):
    found = False
    with open('customer_staff.txt', 'r') as file:
        lines = file.readlines()

    with open('customer_staff.txt', 'w') as file:
        for line in lines:
            if f"username: {username}" in line:  # Adjusted search criteria
                print(f"Staff with username '{username}' deleted successfully.")
                found = True
            else:
                file.write(line)

    if not found:
        print("Staff not found.")

def print_carstaff_data():
    with open('car_service_staff.txt', 'r') as file:
        print()
        print("Car Service Staff List:")
        print()
        lines = file.readlines()
        for line in lines:
            if line.strip():  # Check if the line is not empty
                data = line.strip().split(', ')
                for item in data:
                    key, value = item.split(': ')
                    print(f"{key}: {value}")
                print()
                    

def delete_carstaff_info(username):
    found = False
    with open('car_service_staff.txt', 'r') as file:
        lines = file.readlines()

    with open('car_service_staff.txt', 'w') as file:
        for line in lines:
            if f"username: {username}" in line:  # Adjusted search criteria
                print(f"Staff with username '{username}' deleted successfully.")
                found = True
            else:
                file.write(line)

    if not found:
        print("Staff not found.")

def print_manager_data():
    with open('manager.txt', 'r') as file:
        print()
        print("Manager List:")
        print()
        lines = file.readlines()
        for line in lines:
            if line.strip():  # Check if the line is not empty
                data = line.strip().split(', ')
                for item in data:
                    key, value = item.split(': ')
                    print(f"{key}: {value}")
                print()
                    

def delete_manager_info(username):
    found = False
    with open('Manager.txt', 'r') as file:
        lines = file.readlines()

    with open('Manager.txt', 'w') as file:
        for line in lines:
            if f"username: {username}" in line:  # Adjusted search criteria
                print(f"Staff with username '{username}' deleted successfully.")
                found = True
            else:
                file.write(line)

    if not found:
        print("Staff not found.")

def update_own_profile(username_input):
    # Check for Manager login
    with open('manager.txt', 'r') as file:
        for line in file:                         
                data = line.strip().split(',')
                current_manager = {}
                for info in data:
                    key, value = info.split(':', 1)
                    current_manager[key.strip()] = value.strip()
               # Print the current manager info for debugging
                print()
                print('Your Info:')
                print()
                print("1. Name:", current_manager.get('name'))
                print("2. Age:", current_manager.get('age'))
                print("3. DOB:", current_manager.get('DOB'))
                print("4. Contact information:", current_manager.get('contact information'))
                print("5. Gender:", current_manager.get('gender'))
                print()
                break  # Exit the loop once the manager's info is found

    if not current_manager:
        print("Error: Manager not found.")

def update_manager_info(field, new_value, username):
     # Define the file path
     file_path = 'manager.txt'

     # Read data from the file
     updated_data = []
     updated = False
     with open(file_path, 'r') as file:
         for line in file:
             if f"username: {username}" in line:
                 data = line.strip().split(', ')
                 manager_info = {}
                 for info in data:
                     key, value = info.split(': ')
                     if key.strip() == field:
                         # Update the specified field
                         manager_info[key.strip()] = new_value
                         updated = True
                     else:
                         manager_info[key.strip()] = value.strip()
                         updated_data.append(manager_info)# Append manager_info after processing all fields
                         
             else:
                 updated_data.append(line.strip())

     # Write the updated data back to the file
     with open(file_path, 'w') as file:
         for item in updated_data:
             if isinstance(item, dict):
                 file.write(', '.join([f"{key}: {value}" for key, value in item.items()]) + '\n')
                 break
             else:
                 file.write(item + '\n')

     if updated:
         print("Field updated successfully.")
     else:
         print("Error: Username not found.")


# Main loop

 
if "Login successful. Welcome Manager!" in currentuser:
    while True:
                             
        managermenu()
        try:       
            # Get user input for menu selection
            menuselection = int(input('Select one from (1/2/3/4/5/6/7): '))
            
            # Handle menu selections
            if menuselection == 1:
                    # Code for registering new staff
                staffid = input('Enter New Staff ID: ')
                name = input('Enter New Staff Name: ')
                password = input('Enter New Password: ')
                roleoptions()
                while True:
                    roleoption = int(input('Please Choose One: '))
                    if roleoption in (1, 2, 3):
                        break
                    else:
                        print('invalid option please try again')
                if roleoption == 1:
                    role = 'Customer Service Staff'             
                elif roleoption == 2:
                    role = 'Car Service Staff'
                elif roleoption == 3:
                    role = 'Manager'
                        
                new_user = register(staffid, password, role, name, current_date)
                pass
                    
                    
            elif menuselection == 2:
                    # Code for updating staff details
                    print('''
Select role:
1. Customer Service Staff 
2. Car Service Staff
3. Manager''')
                    while True:
                        updateselection = int(input('Choose one (1/2/3): '))
                        if updateselection in (1, 2, 3):
                            break
                        else:
                            print('Invalid Selection')
                   
                                           
                    if updateselection == 1:
                         updaterole = 'Customer Service Staff'
                      
                         print_customer_staff_1_data()
                         
                         while True:
                             update_customer_staff_1_id = input('Enter the staff username you want to make changes to: ')
                             found = False
                             file_path = 'customer_staff.txt'
                             with open(file_path, 'r') as file:
                                 for line in file:
                                     staff_info = line.strip().split(', ')
                                     staff_dict = {}
                                     for info in staff_info:
                                         key, value = info.split(': ')
                                         staff_dict[key.strip()] = value.strip()
                                     if staff_dict['username'] == update_customer_staff_1_id:
                                         found = True
                                         break
                                    
                             if found:
                                 print('''
Select attribute to update:
1. Username
2. Name
3. Password''')
                                 break         
                         while True:
                                    customer_staff_1_updateselection = int(input('Choose one (1/2/3): '))
                                    if customer_staff_1_updateselection in (1, 2, 3):
                                        break
                                    else:
                                        print('Invalid Selection')
                                        
                       
    
                         if customer_staff_1_updateselection == 1:
                              if found :
                                  new_username = input('Enter the new username: ')
                                  update_staff1_username(updaterole, update_customer_staff_1_id, new_username)
                                  print("Username updated successfully.")
                    
    
                         elif customer_staff_1_updateselection == 2: 
                             if found:
                                 new_name = input('Enter the new name: ')
                                 update_staff_1_name(updaterole, update_customer_staff_1_id, new_name)
                                 print("Name updated successfully.")
                          
        
                         elif customer_staff_1_updateselection == 3:
                             if found:
                                 new_password = input('Enter the new password: ')
                                 update_customer_staff_1_password(updaterole,update_customer_staff_1_id , new_password)
                                 print("Password updated successfully.")
                          
                                         
                    if updateselection == 3:
                         updaterole = 'Manager'
                         print()
                         print("Manager List:")
                         print()
                         file_path = 'manager.txt'
                         with open(file_path, 'r') as file:
                             for line in file:
                                 staff_info = line.strip().split(', ')
                                 staff_dict = {}
                                 for info in staff_info:
                                     key, value = info.split(': ')
                                     staff_dict[key.strip()] = value.strip()
                                 print("Username:", staff_dict['username'])
                                 print("Name:", staff_dict['name'])
                                 print("Password:", staff_dict['password'])
                                 print("Role:", staff_dict['role'])
                              
                                 print()
                         
                         while True:
                             updatemanagerid = input('Enter the staff username you want to make changes to: ')
                             found = False
                             with open(file_path, 'r') as file:
                                 for line in file:
                                     staff_info = line.strip().split(', ')
                                     staff_dict = {}
                                     for info in staff_info:
                                         key, value = info.split(': ')
                                         staff_dict[key.strip()] = value.strip()
                                     if staff_dict['username'] == updatemanagerid:
                                         found = True
                                         break
                             if found:
                                        print('''
Select attribute to update:
1. Username
2. Name
3. Password''')
                                        break
                         while True:
                                    managerupdateselection = int(input('Choose one (1/2/3): '))
                                    if managerupdateselection in (1, 2, 3):
                                        break
                                    else:
                                        print('Invalid Selection')
                                        
                             
    
                         if managerupdateselection == 1:
                              if found :
                                  new_username = input('Enter the new username: ')
                                  update_manager_username(updaterole, updatemanagerid, new_username)
                                  print("Username updated successfully.")
    
                         elif managerupdateselection == 2: 
                             if found:
                                 new_name = input('Enter the new name: ')
                                 update_manager_name(updaterole, updatemanagerid, new_name)
                                 print("Name updated successfully.")
      
                                
    
    
                         elif managerupdateselection == 3:
                             if found:
                                 new_password = input('Enter the new password: ')
                                 update_manager_password(updaterole, updatemanagerid, new_password)
                                 print("Password updated successfully.")
                      
                    if updateselection == 2:
                        updaterole = 'Car Service Staff'
                        print()
                        print("Car Service Staff  List:")
                        print()
                        file_path = 'car_service_staff.txt'
                        with open(file_path, 'r') as file:
                            for line in file:
                                staff_info = line.strip().split(', ')
                                staff_dict = {}
                                for info in staff_info:
                                    key, value = info.split(': ')
                                    staff_dict[key.strip()] = value.strip()
                                print("Username:", staff_dict['username'])
                                print("Name:", staff_dict['name'])
                                print("Password:", staff_dict['password'])
                                print("Role:", staff_dict['role'])
                             
                                print()
                        
                        while True:
                            updatecarstaffid = input('Enter the staff username you want to make changes to: ')
                            found = False
                            with open(file_path, 'r') as file:
                                for line in file:
                                    staff_info = line.strip().split(', ')
                                    staff_dict = {}
                                    for info in staff_info:
                                        key, value = info.split(': ')
                                        staff_dict[key.strip()] = value.strip()
                                    if staff_dict['username'] == updatecarstaffid:
                                        found = True
                                        break

                                
                                if found:
                                    print('''
Select attribute to update:
1. Username
2. Name
3. Password''')
                                
                                    break
    
                        while True:
                                    carstaffupdateselection = int(input('Choose one (1/2/3): '))
                                    if carstaffupdateselection in (1, 2, 3):
                                        break
                                    else:
                                        print('Invalid Selection')
                        else:
                                     print('Invalid Username')
                                        
                    
    
                        if carstaffupdateselection == 1:
                                    if found :
                                        new_username = input('Enter the new username: ')
                                        update_carstaff_username(updaterole, updatecarstaffid, new_username)
                                        print("Username updated successfully.")
            
    
                        elif carstaffupdateselection == 2:      
                                   if found:
                                       new_name = input('Enter the new name: ')
                                       update_carstaff_name(updaterole, updatecarstaffid, new_name)
                                       print("Name updated successfully.")
    
                        elif carstaffupdateselection == 3:
                                    if found:
                                        new_password = input('Enter the new password: ')
                                        update_carstaff_password(updaterole, updatecarstaffid, new_password)
                                        print("Password updated successfully.")
                             
                   
                        
                    
                        
                # Handle other menu selections
            elif menuselection == 3:
                    # Code for deleting staff record
                    roleoptions()
                    while True:   
                        dltroleoption =int(input('choose one from (1/2/3): '))
                        if dltroleoption in (1,2,3):
                            break
                        else :
                            print('Invalid Option')
                            
                    if dltroleoption == 1:                      
                        print_customer_staff_1_data()
                        username_to_delete = input("Enter the username you want to delete: ")
                        delete_staff1_info(username_to_delete)
                                                                                                                 
                    if dltroleoption == 2:
                        print_carstaff_data()
                        username_to_delete = input("Enter the username you want to delete: ")
                        delete_carstaff_info(username_to_delete)
                                                   
                    if dltroleoption == 3:                      
                        print_manager_data()
                        username_to_delete = input("Enter the username you want to delete: ")
                        delete_manager_info(username_to_delete)
                     
                    
                    
                        
                        
                 
            elif menuselection == 4:               
                with open('car_renting_rates.txt', 'w') as file:  # Open file in write mode to overwrite previous data
        # Prompt the user to input the renting rates for different types of cars
                    print('Enter Car Renting Rates')
                    passenger_4 = int(input('4 passenger car renting rate: '))
                    file.write(f"Passenger: 4, Rate: {passenger_4}\n")
                    
                    passenger_7 = int(input('7 passenger car renting rate: '))
                    file.write(f"Passenger: 7, Rate: {passenger_7}\n")

                    passenger_9 = int(input('9 passenger car renting rate: '))
                    file.write(f"Passenger: 9, Rate: {passenger_9}\n")

                    print('\nThe List Of Car Renting Rate')
                    print(f"4 passenger car is: {passenger_4}")
                    print(f"7 passenger car is: {passenger_7}")
                    print(f"9 passenger car is: {passenger_9}")

            elif menuselection == 5:
                print()
                print('The List Of Car Renting Rate ')

    # Print the existing car renting rates from the file
                with open('car_renting_rates.txt', 'r') as file:
                    for line in file:
                        print(line.strip())

                while True:
                    updaterentingrate = int(input('Select one from (4/7/9): '))
                    if updaterentingrate in (4, 7, 9):
                        break
                    else:
                        print('Invalid Selection')

                if updaterentingrate == 4:
                    print()
                    print('Old 4 passenger car rate is:', passenger_4)
                   
                    with open('car_renting_rates.txt', 'w') as file:  # Open file in write mode to overwrite previous data
            # Prompt the user to input the renting rates for different types of cars
                        passenger_4 = int(input('4 passenger car renting rate: '))
                        file.write(f"Passenger: 4, Rate: {passenger_4}\n")
                        file.write(f"Passenger: 7, Rate: {passenger_7}\n")
                        file.write(f"Passenger: 9, Rate: {passenger_9}\n")
                    print()
                    print('Renting Rate Changed Successfully')
                    print('4 passenger car renting rate:', passenger_4)
                
                if updaterentingrate == 7:
                    print()
                    print('Old 7 passenger car rate is:', passenger_7)
                   
                    with open('car_renting_rates.txt', 'w') as file:  # Open file in write mode to overwrite previous data
            # Prompt the user to input the renting rates for different types of cars
                        passenger_7 = int(input('7 passenger car renting rate: '))
                        file.write(f"Passenger: 4, Rate: {passenger_4}\n")
                        file.write(f"Passenger: 7, Rate: {passenger_7}\n")
                        file.write(f"Passenger: 9, Rate: {passenger_9}\n")
                    print()
                    print('Renting Rate Changed Successfully')
                    print('7 passenger car renting rate:', passenger_7)
                
                if updaterentingrate == 9:
                    print()
                    print('Old 9 passenger car rate is:', passenger_7)
                   
                    with open('car_renting_rates.txt', 'w') as file:  # Open file in write mode to overwrite previous data
            # Prompt the user to input the renting rates for different types of cars
                        passenger_9 = int(input('9 passenger car renting rate: '))
                        file.write(f"Passenger: 4, Rate: {passenger_4}\n")
                        file.write(f"Passenger: 7, Rate: {passenger_7}\n")
                        file.write(f"Passenger: 9, Rate: {passenger_9}\n")
                    print()
                    print('Renting Rate Changed Successfully')
                    print('9 passenger car renting rate:', passenger_9)


  

                   

                    
                        
            elif menuselection == 6:
                while True:
                        try:
                            year = int(input("Enter the year: "))
                            month = int(input("Enter the month (1-12): "))
                            if 1 <= month <= 12:
                                break
                            else:
                                print("Invalid month. Please enter a number between 1 and 12.")
                        except ValueError:
                            print("Invalid input. Please enter a valid year and month.")

                view_monthly_revenue(year, month)
                    # Code for viewing monthly revenue report
                    
            elif menuselection == 7:
                update_own_profile(username_input)          
    # Example usage:
                managerinfoselection = int(input('Select one from (1/2/3/4/5): '))
                while True:
                       if managerinfoselection in (1, 2, 3, 4, 5):
                           break
                       else:
                           print('Invalid Selection')
                           managerinfoselection = int(input('Select one from (1/2/3/4/5): '))
                                       
                if managerinfoselection == 1:
                       newinfoname = input('Enter Your New Name: ')
                       update_manager_info('name', newinfoname, username_input)

                if managerinfoselection == 2:
                       newinfoage = input('Enter Your New Age: ')
                       update_manager_info('age', newinfoage, username_input)

                if managerinfoselection == 3:
                       newinfoDOB = input('Enter Your New DOB (DD MM YYYY): ')
                       update_manager_info('DOB', newinfoDOB, username_input)

                if managerinfoselection == 4:
                       newinfoCI = input('Enter Your New Contact information: ')
                       update_manager_info('contact information', newinfoCI, username_input)

                if managerinfoselection == 5:
                       newinfogender = input('Enter Your New Gender (Male/Female): ')
                       update_manager_info('gender', newinfogender, username_input)

            else:
                print("Invalid selection. Please select a number from 1 to 7.")
             
            # Ask if the user wants to continue or exit
            while True :
                
                choice = input("Do you want to continue? (yes/no): ")
                if choice in ('yes', 'no'):
                    break
                else:
                    print()
                    print('Enter yes or no only')
                    
            if choice.lower() != 'yes':
                break  # Exit the loop if the user doesn't want to continue
        except ValueError:
              print("Invalid input. Please enter a number.")

carinfo_file = 'carinfo.txt'

# to register the car
def carstaffregister(car_reg, car_man, car_model, yom, seatcap, lastserviced, IPnumber, Iexpirydate, roadtaxexpirydate, available, car_renting_rate, return_date):
    new_car_info = {'carregistration': car_reg, 'carmanufacturer': car_man, 'carmodel': car_model, 'yearofmanufacturer': yom, 'seatingcapacity': seatcap, 'lastservicedate': lastserviced, 'insurancepolicynumber': IPnumber, 'insuranceexpirydate': Iexpirydate, 'roadtaxexpirydate': roadtaxexpirydate, 'availability': available, 'car renting rate': car_renting_rate, 'returndate': return_date}
    with open(carinfo_file, 'a') as file:
        formatted_item = ', '.join([f"{key}: {value}" for key, value in new_car_info.items()])
        file.write(formatted_item + '\n')
# extract all the data from the text file
def print_car_info_from_file(file_path):
                with open(file_path, 'r') as file:
                    print()
                    print("Car Information:")
                    for line in file:
                        car_data = line.strip().split(', ')
                        car_info = {}
                        for item in car_data:
                            key, value = item.split(': ')
                            car_info[key.strip()] = value.strip()
                        print("Car Registration:", car_info['carregistration'])
                        print("Manufacturer:", car_info['carmanufacturer'])
                        print("Model:", car_info['carmodel'])
                        print("Year of Manufacture:", car_info['yearofmanufacturer'])
                        print("Seating Capacity:", car_info['seatingcapacity'])
                        print("Last Service Date:", car_info['lastservicedate'])
                        print("Insurance Policy Number:", car_info['insurancepolicynumber'])
                        print("Insurance Expiry Date:", car_info['insuranceexpirydate'])
                        print("Road Tax Expiry Date:", car_info['roadtaxexpirydate'])
                        print("Availability:", car_info['availability'])
                        print("Car Renting Rate:", car_info['car renting rate'])
                        print("Return Date:", car_info['returndate'])
                        print()

# print all the car from the text file with the availability = 'Available'
file_path = 'carinfo.txt'
def print_available_car_info_from_file(file_path):
                with open(file_path, 'r') as file:
                    print()
                    print("Available Car Information:")
                    for line in file:
                        car_data = line.strip().split(', ')
                        car_info = {}
                        for item in car_data:
                            key, value = item.split(': ')
                            car_info[key.strip()] = value.strip()
                        if car_info.get('availability') == 'Available':
                            print("Car Registration:", car_info['carregistration'])
                            print("Manufacturer:", car_info['carmanufacturer'])
                            print("Model:", car_info['carmodel'])
                            print("Year of Manufacture:", car_info['yearofmanufacturer'])
                            print("Seating Capacity:", car_info['seatingcapacity'])
                            print("Last Service Date:", car_info['lastservicedate'])
                            print("Insurance Policy Number:", car_info['insurancepolicynumber'])
                            print("Insurance Expiry Date:", car_info['insuranceexpirydate'])
                            print("Road Tax Expiry Date:", car_info['roadtaxexpirydate'])
                            print("Availability:", car_info['availability'])
                            print("Car Renting Rate:", car_info['car renting rate'])
                            print("Return Date:", car_info['returndate'])
                            print()


file_path = 'carinfo.txt'
 # print all the car from the text file with the availability 'Rented'           
def print_rented_car_info_from_file(file_path):
                with open(file_path, 'r') as file:
                    print()
                    print("Rented Car Information:")
                    for line in file:
                        car_data = line.strip().split(', ')
                        car_info = {}
                        for item in car_data:
                            key, value = item.split(': ')
                            car_info[key.strip()] = value.strip()
                        if car_info.get('availability') == 'Rented':
                            print("Car Registration:", car_info['carregistration'])
                            print("Manufacturer:", car_info['carmanufacturer'])
                            print("Model:", car_info['carmodel'])
                            print("Year of Manufacture:", car_info['yearofmanufacturer'])
                            print("Seating Capacity:", car_info['seatingcapacity'])
                            print("Last Service Date:", car_info['lastservicedate'])
                            print("Insurance Policy Number:", car_info['insurancepolicynumber'])
                            print("Insurance Expiry Date:", car_info['insuranceexpirydate'])
                            print("Road Tax Expiry Date:", car_info['roadtaxexpirydate'])
                            print("Availability:", car_info['availability'])
                            print("Car Renting Rate:", car_info['car renting rate'])
                            print("Return Date:", car_info['returndate'])
                            print()

# Specify the path to your text file
file_path = 'carinfo.txt'

 # menu for car staff  
def carstaffmenu():
    print('''
Menu
1.Register New Cars
2.Update Car Details
3.View Cars
4.Delete Car
5.Update Own Profile''')
#update function
def update_insurance_policy_number(registration_number, new_policy_number, file_path):
    updated = False
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            car_data = line.strip().split(', ')
            car_info = {}
            for item in car_data:
                key, value = item.split(': ')
                car_info[key.strip()] = value.strip()
            if car_info.get('carregistration') == registration_number:
                car_info['insurancepolicynumber'] = new_policy_number
                updated = True
                updated_car_info = car_info
            file.write(', '.join([f"{key}: {value}" for key, value in car_info.items()]) + '\n')

    if updated:
        print("Insurance policy number updated successfully.")
        print()
        print("Updated car information:")
        for key, value in updated_car_info.items():
            print(f"{key}: {value}")
    else:
        print("Car with the given registration number not found.")
        file_path = 'carinfo.txt'
 #update function       
def update_insurance_expiry_date(registration_number, new_expiry_date, file_path):
    updated_car_info = None
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        with open(file_path, 'w') as file:
            for line in lines:
                car_data = line.strip().split(', ')
                car_info = {}
                for item in car_data:
                    key, value = item.split(': ')
                    car_info[key.strip()] = value.strip()
                if car_info.get('carregistration') == registration_number:
                    car_info['insuranceexpirydate'] = new_expiry_date
                    updated_car_info = car_info
                file.write(', '.join([f"{key}: {value}" for key, value in car_info.items()]) + '\n')

        if updated_car_info:
            print("Insurance expiry date updated successfully.")
            print()
            print("Updated car information:")
            for key, value in updated_car_info.items():
                print(f"{key}: {value}")
        else:
            print("Car with the given registration number not found.")
#update function
def update_roadtax_expiry_date(registration_number, roadtax_expiry_date, file_path):
     updated_car_info = None
     with open(file_path, 'r') as file:
         lines = file.readlines()
         
         with open(file_path, 'w') as file:
             for line in lines:
                 car_data = line.strip().split(', ')
                 car_info = {}
                 for item in car_data:
                     key, value = item.split(': ')
                     car_info[key.strip()] = value.strip()
                 if car_info.get('carregistration') == registration_number:
                     car_info['roadtaxexpirydate'] = roadtax_expiry_date
                     updated_car_info = car_info
                 file.write(', '.join([f"{key}: {value}" for key, value in car_info.items()]) + '\n')

         if updated_car_info:
             print("Road Tax expiry date updated successfully.")
             print()
             print("Updated car information:")
             for key, value in updated_car_info.items():
                 print(f"{key}: {value}")
         else:
             print("Car with the given registration number not found.")
#update function
def update_renting_rate(registration_number, new_renting_rate, file_path):
    updated_car_info = None
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            car_data = line.strip().split(', ')
            car_info = {}
            for item in car_data:
                key, value = item.split(': ')
                car_info[key.strip()] = value.strip()
            if car_info.get('carregistration') == registration_number:
                car_info['car renting rate'] = new_renting_rate
                updated_car_info = car_info
            file.write(', '.join([f"{key}: {value}" for key, value in car_info.items()]) + '\n')

        if updated_car_info:
            print("Renting rate updated successfully.")
            print()
            print("Updated car information:")
            for key, value in updated_car_info.items():
                print(f"{key}: {value}")
        else:
            print("Car with the given registration number not found.")
#update function
def update_availability(registration_number, new_availability, file_path):
    updated_car_info = None
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    with open(file_path, 'w') as file:
        for line in lines:
            car_data = line.strip().split(', ')
            car_info = {}
            for item in car_data:
                key, value = item.split(': ')
                car_info[key.strip()] = value.strip()
            if car_info.get('carregistration') == registration_number:
                car_info['availability'] = new_availability
                updated_car_info = car_info
            file.write(', '.join([f"{key}: {value}" for key, value in car_info.items()]) + '\n')

        if updated_car_info:
            print("Availability updated successfully.")
            print()
            print("Updated car information:")
            for key, value in updated_car_info.items():
                print(f"{key}: {value}")
        else:
            print("Car with the given registration number not found.")
def update_return_date(registration_number, new_return_date, file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    with open(file_path, 'w') as file:
        for line in lines:
            car_data = line.strip().split(', ')
            car_info = {}
            for item in car_data:
                key, value = item.split(': ')
                car_info[key.strip()] = value.strip()
            if car_info.get('carregistration') == registration_number:
                car_info['returndate'] = new_return_date
            file.write(', '.join([f"{key}: {value}" for key, value in car_info.items()]) + '\n')


def update_last_service_date(registration_number, new_last_service_date, file_path):
   
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    with open(file_path, 'w') as file:
        for line in lines:
            car_data = line.strip().split(', ')
            car_info = {}
            for item in car_data:
                key, value = item.split(': ')
                car_info[key.strip()] = value.strip()
            if car_info.get('carregistration') == registration_number:
                car_info['lastservicedate'] = new_last_service_date
            file.write(', '.join([f"{key}: {value}" for key, value in car_info.items()]) + '\n')
            
    

if"Login successful. Welcome Car Service Staff!" in currentuser :
    while True :
        carstaffmenu()                   
        carstaffmenuselection = int(input('Please choose one from (1/2/3/4/5): '))
            
        # request basic information for register       
        if carstaffmenuselection == 1 :
            car_reg = input('Please Enter New Car Registration No, for example, KVE2926: ').upper()
            car_man = input('Please Enter New Car Manufacturer, for example, PERODUA: ').upper()
            car_model = input('Please Enter New Car Model, for example, BEZZA: ').upper()
            yom = input('Please Enter New Car Year Of Manufacturer, for example, 2016: ')
            availability =('Available')
            car_renting_rate = None
            return_date = None
            filename = 'car_renting_rates.txt'
              
            
            while True:
                seatcap = input('Please Enter One Seating Capacity From (4/7/9): ')
                if seatcap in ('4', '7', '9'):
                    break
                else:
                    print('Invalid Selection')

            # Open the file and search for the renting rate
            try:
                with open(filename, 'r') as file:
                    for line in file:
                        if line.strip().startswith(f"Passenger: {seatcap}"):
                            car_renting_rate = int(line.split(": ")[-1].strip())
                            break
            except FileNotFoundError:
                print("Error: File not found.")
                # Handle the case where the file does not exist
            except Exception as e:
                print("An error occurred:", e)
                # Handle other exceptions

            # Check if car_renting_rate has been updated
            if car_renting_rate is not None:
                print(f"Renting rate for {seatcap} passenger car:", car_renting_rate)
            else:
                print(f"Error: Renting rate for {seatcap} passenger car not found.")
                # Handle the case where the renting rate is not found

# Check if car_renting_rate has been update
            while True:
                lastserviced = input('Please Enter The New Car Last Service Date in (DDMMYYYY), for example, 30 12 2023: ')
                lastserviced_parts = lastserviced.split()
                if len(lastserviced_parts) == 3:
                    if all(part.isdigit() for part in lastserviced_parts):
                        day, month, year = lastserviced_parts
                        try:
                            datetime.datetime(int(year), int(month), int(day))
                            break
                        except ValueError:
                            print("Invalid date. Please enter a valid date.")
                    else:
                        print("Invalid input format. Please enter numbers for day, month, and year.")
                else:
                    print("Invalid input format. Please enter day, month, and year separated by spaces.")
            IPnumber = input('Please Enter New Car Insurance Policy Number, for example, XA123456: ').upper()
            while True:
                Iexpirydate = input('Please Enter The New Car Insurance Expiry Date in (DDMMYYYY), for example, 30 12 2023: ')
                Iexpirydate_parts = Iexpirydate.split()
                if len(Iexpirydate_parts) == 3:
                    if all(part.isdigit() for part in Iexpirydate_parts):
                        day, month, year = Iexpirydate_parts
                        try:
                            datetime.datetime(int(year), int(month), int(day))
                            break
                        except ValueError:
                            print("Invalid date. Please enter a valid date.")
                    else:
                        print("Invalid input format. Please enter numbers for day, month, and year.")
                else:
                    print("Invalid input format. Please enter day, month, and year separated by spaces.")
            while True:
                roadtaxexpirydate = input('Please Enter The New Car Road Tax Expiry Date in (DDMMYYYY), for example, 30 12 2023: ')
                roadtaxexpirydate_parts = roadtaxexpirydate.split()
                if len(roadtaxexpirydate_parts) == 3:
                    if all(part.isdigit() for part in roadtaxexpirydate_parts):
                        day, month, year = roadtaxexpirydate_parts
                        try:
                            datetime.datetime(int(year), int(month), int(day))
                            break
                        except ValueError:
                            print("Invalid date. Please enter a valid date.")
                    else:
                        print("Invalid input format. Please enter numbers for day, month, and year.")
                else:
                    print("Invalid input format. Please enter day, month, and year separated by spaces.")
            carstaffregister(car_reg, car_man, car_model, yom, seatcap, lastserviced, IPnumber, Iexpirydate, roadtaxexpirydate,availability,car_renting_rate,return_date)
            print("\nNew Car Information:")
            print("Registration No:", car_reg)
            print("Manufacturer:", car_man)
            print("Model:", car_model)
            print("Year Of Manufacturer:", yom)
            print("Seating Capacity:", seatcap)
            print("Last Service Date:", lastserviced)
            print("Insurance Policy Number:", IPnumber)
            print("Insurance Expiry Date:", Iexpirydate)
            print("Road Tax Expiry Date:", roadtaxexpirydate)
            print('Availability: ', availability)
            print('Car Renting Rate: ',car_renting_rate)
            pass
        
        elif carstaffmenuselection == 2 :
           

#Print update menu

                    
            print('''
UPDATE MENU                  
1.Insurance Policy Number
2.Insurance Expiry Date
3.Road Tax Expiry Date
4.Car Renting Rate per day
5.Rental Availability        ''')
            while True :
                carlistselection = int(input('Select one from (1/2/3/4/5): '))
                if carlistselection in (1,2,3,4,5):
                    break
                else :
                    print('Invalid Selection')
            
            if carlistselection == 1:
                file_path = 'carinfo.txt'
                print_car_info_from_file('carinfo.txt')
                registration_number = input('Enter the car registration number you want to make changes to: ')
                new_policy_number = input('Enter new Insurance Policy Number: ').upper()
                update_insurance_policy_number(registration_number, new_policy_number, file_path)
            if carlistselection == 2 :
                file_path = 'carinfo.txt'
                print_car_info_from_file('carinfo.txt')
                registration_number = input('Enter the car registration number you want to make changes to: ')
                while True :
                    new_expiry_date = input('Enter new Insurance Expiry Date: ')
                    new_expiry_date_parts =  new_expiry_date.split()
                    if len( new_expiry_date_parts) == 3:
                        if all(part.isdigit() for part in  new_expiry_date_parts):
                            day, month, year =  new_expiry_date_parts
                            try:
                                datetime.datetime(int(year), int(month), int(day))
                                break
                            except ValueError:
                                print("Invalid date. Please enter a valid date.")
                        else:
                            print("Invalid input format. Please enter numbers for day, month, and year.")
                    else:
                        print("Invalid input format. Please enter day, month, and year separated by spaces.")
                
                update_insurance_expiry_date(registration_number, new_expiry_date, file_path)
            if carlistselection == 3 :
                file_path = 'carinfo.txt'
                print_car_info_from_file('carinfo.txt')
                registration_number = input('Enter the car registration number you want to make changes to: ')
                while True :
                    roadtax_expiry_date = input('Enter new Road Tax Expiry Date: ')
                    roadtax_expiry_date_parts =  roadtax_expiry_date.split()
                    if len( roadtax_expiry_date_parts) == 3:
                        if all(part.isdigit() for part in  roadtax_expiry_date_parts):
                            day, month, year =  roadtax_expiry_date_parts
                            try:
                                datetime.datetime(int(year), int(month), int(day))
                                break
                            except ValueError:
                                print("Invalid date. Please enter a valid date.")
                        else:
                            print("Invalid input format. Please enter numbers for day, month, and year.")
                    else:
                        print("Invalid input format. Please enter day, month, and year separated by spaces.")
                
                update_roadtax_expiry_date(registration_number, roadtax_expiry_date, file_path) 
            if carlistselection == 4 :
                file_path = 'carinfo.txt'
                print_car_info_from_file('carinfo.txt')
                registration_number = input('Enter the car registration number you want to make changes to: ')
                new_renting_rate = input('Enter new renting rate: ')
                update_renting_rate(registration_number, new_renting_rate, file_path)
            if carlistselection == 5 :
                file_path = 'carinfo.txt'
                print_car_info_from_file('carinfo.txt')
                registration_number = input('Enter the car registration number you want to make changes to: ')
                while True :
                    new_availability = input('Enter availability from (Available/Reserved/Rented/Under Service/Disposed): ')
                    if new_availability in ('Available','Reserved','Rented','Under Service','Disposed'):
                        break
                    else :
                        print('Invalid Selection')
                if new_availability == 'Rented' :
                    while True :
                        new_return_date = input('Enter the date of return: ')
                        new_return_date_parts =   new_return_date.split()
                        if len(  new_return_date_parts) == 3:
                            if all(part.isdigit() for part in   new_return_date_parts):
                                day, month, year =   new_return_date_parts
                                try:
                                    datetime.datetime(int(year), int(month), int(day))
                                    break
                                except ValueError:
                                    print("Invalid date. Please enter a valid date.")
                            else:
                                print("Invalid input format. Please enter numbers for day, month, and year.")
                        else:
                            print("Invalid input format. Please enter day, month, and year separated by spaces.")
                    
                        
                   
                    update_return_date(registration_number, new_return_date, file_path)
                    update_availability(registration_number, new_availability, file_path)
                if new_availability == 'Under Service':
                   while True :
                       new_last_service_date = input('Enter the date of return: ')
                       new_last_service_date_parts =   new_last_service_date.split()
                       if len(  new_last_service_date_parts) == 3:
                           if all(part.isdigit() for part in  new_last_service_date_parts):
                               day, month, year =   new_last_service_date_parts
                               try:
                                   datetime.datetime(int(year), int(month), int(day))
                                   break
                               except ValueError:
                                   print("Invalid date. Please enter a valid date.")
                           else:
                               print("Invalid input format. Please enter numbers for day, month, and year.")
                       else:
                           print("Invalid input format. Please enter day, month, and year separated by spaces.")
                
                   update_last_service_date(registration_number, new_last_service_date, file_path)
                   update_availability(registration_number, new_availability, file_path)
                    
                
                if new_availability in ('Available','Reserved','Disposed'):    
                    update_availability(registration_number, new_availability, file_path)
            
                
                
                
            

            
            
                               
        
                
        elif carstaffmenuselection == 3 :
            print('''
1.View All Car
2.Car Available for rent
3.Rented Car                 ''')
            while True :
                carlistselection = int(input('Select one from (1/2/3): '))
                if carlistselection in (1,2,3):
                    break
                else :
                    print('Invalid Selection')
            if carlistselection == 1 :
                print_car_info_from_file('carinfo.txt')
            if carlistselection == 2 :
                print_available_car_info_from_file(file_path)
                
            if carlistselection == 3 :
                print_rented_car_info_from_file(file_path)
                #print_rented_carinfo('carinfo.txt')
            
        elif carstaffmenuselection == 4 :
            def print_disposed_car_info(file_path):
                print()
                print("Disposed Car Information:")
                with open(file_path, 'r') as file:
                    for line in file:
                        car_data = line.strip().split(', ')
                        car_info = {}
                        for item in car_data:
                            key, value = item.split(': ')
                            car_info[key.strip()] = value.strip()
                        if car_info.get('availability') == 'Disposed':
                            print("Car Registration:", car_info.get('carregistration'))
                            print("Manufacturer:", car_info.get('carmanufacturer'))
                            print("Model:", car_info.get('carmodel'))
                            print("Year of Manufacture:", car_info.get('yearofmanufacturer'))
                            print("Seating Capacity:", car_info.get('seatingcapacity'))
                            print("Last Service Date:", car_info.get('lastservicedate'))
                            print("Insurance Policy Number:", car_info.get('insurancepolicynumber'))
                            print("Insurance Expiry Date:", car_info.get('insuranceexpirydate'))
                            print("Road Tax Expiry Date:", car_info.get('roadtaxexpirydate'))
                            print("Availability:", car_info.get('availability'))
                            print("Car Renting Rate:", car_info.get('car renting rate'))
                            print("Return Date:", car_info.get('returndate'))
                            print()


            file_path = 'carinfo.txt'
            print_disposed_car_info(file_path)
            def delete_disposed_car_by_registration(file_path):
                registration_number = input("Enter the registration number of the car you want to delete: ")
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                with open(file_path, 'w') as file:
                    car_deleted = False
                    for line in lines:
                        car_data = line.strip().split(', ')
                        car_info = {}
                        for item in car_data:
                            key, value = item.split(': ')
                            car_info[key.strip()] = value.strip()
                        if car_info.get('carregistration') == registration_number and car_info.get('availability') == 'Disposed':
                                print(f"Car with registration number '{registration_number}' deleted successfully.")
                                car_deleted = True
                        else:
                                file.write(line)

                    if not car_deleted:
                        print("Car not found or not disposed.")
            delete_disposed_car_by_registration('carinfo.txt')

            

             
            pass
        elif carstaffmenuselection == 5 :
            def update_carstaff_own_profile(username_input):
                # Check for Manager login
                with open('car_service_staff.txt', 'r') as file:
                    for line in file:
                            data = line.strip().split(',')
                            current_carstaff = {}
                            for info in data:
                                key, value = info.split(':', 1)
                                current_carstaff[key.strip()] = value.strip()
                           # Print the current manager info for debugging
                            print()
                            print('Your Info:')
                            print()
                            print("1. Name:", current_carstaff.get('name'))
                            print("2. Age:", current_carstaff.get('age'))
                            print("3. DOB:", current_carstaff.get('DOB'))
                            print("4. Contact information:", current_carstaff.get('contact information'))
                            print("5. Gender:", current_carstaff.get('gender'))
                            print()
                            break  # Exit the loop once the manager's info is found

                if not current_carstaff:
                    print("Error: Manager not found.")
            update_carstaff_own_profile(username_input)


      

# Example usage:
        
            while True:
                   carstaffinfoselection = int(input('Select one from (1/2/3/4/5): '))
                   if carstaffinfoselection in (1, 2, 3, 4, 5):
                       break
                   else:
                       print('Invalid Selection')
                       
            def update_carstaff_info(field, new_value, username):
# Define the file path
                file_path = 'car_service_staff.txt'

# Read data from the file
                updated_data = []
                updated = False
                with open(file_path, 'r') as file:
                    for line in file:
                        if f"username: {username}" in line:
                            data = line.strip().split(', ')
                            carstaff_info = {}
                            for info in data:
                                key, value = info.split(': ')
                                if key.strip() == field:
                                    # Update the specified field
                                    carstaff_info[key.strip()] = new_value
                                    updated = True
                                else:
                                    carstaff_info[key.strip()] = value.strip()
                                    updated_data.append(carstaff_info)# Append manager_info after processing all fields
                                    
                        else:
                            updated_data.append(line.strip())

# Write the updated data back to the file
                with open(file_path, 'w') as file:
                    for item in updated_data:
                        if isinstance(item, dict):
                            file.write(', '.join([f"{key}: {value}" for key, value in item.items()]) + '\n')
                            break
                        else:
                            file.write(item + '\n')

                if updated:
                    print("Field updated successfully.")
                else:
                    print("Error: Username not found.")
                        
            if carstaffinfoselection == 1:
                       newinfoname = input('Enter Your New Name: ')
                       update_carstaff_info('name', newinfoname, username_input)

            if carstaffinfoselection == 2:
                       newinfoage = input('Enter Your New Age: ')
                       update_carstaff_info('age', newinfoage, username_input)

            if carstaffinfoselection == 3:
                       newinfoDOB = input('Enter Your New DOB (DD MM YYYY): ')
                       update_carstaff_info('DOB', newinfoDOB, username_input)

            if carstaffinfoselection == 4:
                       newinfoCI = input('Enter Your New Contact information: ')
                       update_carstaff_info('contact information', newinfoCI, username_input)

            if carstaffinfoselection == 5:
                       newinfogender = input('Enter Your New Gender (Male/Female): ')
                       update_carstaff_info('gender', newinfogender, username_input)


            
            pass
        else:
            print("Invalid selection. Please select a number from 1 to 5.")

        # Ask if the user wants to continue or exit
        while True :
            
            choice = input("Do you want to continue? (yes/no): ")
            if choice in ('yes','no'):
                break
            else:
                print()
                print('Enter yes or no only')
                
        if choice.lower() != 'yes':
            break  # Exit the loop if the user doesn't want to continue
        

if"Login successful. Welcome Customer Service Staff!" in currentuser :
    class Customer:
        def __init__(self, customer_id, name, nric=None, passport=None, license=None, address="", phone=""):   # Initialize customer attributes
            self.customer_id = customer_id  # Unique identifier for the customer
            self.name = name  # Name of the customer
            self.nric = nric  # National Registration Identity Card number (optional)
            self.passport = passport # Passport number (optional)
            self.license = license  # Driver's license number (optional)
            self.address = address  # Customer's address
            self.phone = phone  # Customer's phone number
            self.registration_date = datetime.datetime.now().strftime("%d-%m-%Y")  # Today's date
    
    class Car:
        def __init__(self, reg_number, manufacturer, model, year, passenger_count, rental_price, status):  # Initialize car attributes
            self.reg_number = reg_number  # Vehicle registration number
            self.manufacturer = manufacturer  # Car manufacturer
            self.model = model   # Car model
            self.year = year  # Year of manufacture
            self.passenger_count = passenger_count  # Number of passengers the car can accommodate
            self.rental_price = rental_price   # Rental price per day
            self.status = status  # Availability status of the car


    class RentalTransaction:
        def __init__(self, car_reg_number, customer_id, rental_date, return_date, total_rental=0):   # Initialize rental transaction attributes
            self.car_reg_number = car_reg_number  # Vehicle registration number of the rented car
            self.customer_id = customer_id   # Identifier of the customer renting the car
            self.rental_date = rental_date   # Date when the car is rented
            self.return_date = return_date    # Date when the car is returned
            self.rental_periods = (return_date - rental_date).days   # Duration of the rental period in days
            self.total_rental = total_rental  # Total rental cost for the transaction


    class Bill:
        def __init__(self, customer_id, total_amount):  # Initialize bill attributes
            self.customer_id = customer_id  # Identifier of the customer
            self.total_amount = total_amount  # Total amount due in the bill


    def generate_bill(transaction, file_path_rentals):
        # This function generates a bill for a rental transaction and writes it to a file.
        # It retrieves customer ID and car registration number from the rental transaction,
        # reads car rental data from the file, extracts total rental amount, creates a new bill object,
        # writes bill information to a file, and prints a confirmation message.
        # If no rental transaction is found for the entered customer ID, it prints a message and returns None.
        customer_id = transaction.customer_id
        car_reg_number = transaction.car_reg_number
        
        # Read car rental data from the file
        with open(file_path_rentals, 'r') as file:
            for line in file:
                if f"Customer ID: {customer_id}, Car Registration Number: {car_reg_number}" in line:
                    # Extract total rental amount from the line
                    total_rental_amount = float(line.split("Total Rental: ")[1].split(" ")[0].replace("RM", "").replace(",", ""))
                    
                    # Create a new bill object
                    new_bill = Bill(customer_id, total_rental_amount)
                    
                    # Write bill information to the bill.txt file
                    with open('bill.txt', 'a') as bill_file:
                        bill_file.write(f"Customer ID: {customer_id}, Total Amount: RM{total_rental_amount:.2f}\n")
                    
                    print(f"Bill generated for customer ID {customer_id}. Total Amount: RM{total_rental_amount:.2f}")
                    
                    return new_bill
        
        print("No rental transaction found for the entered customer ID.")
        return None


    def accept_payment(bill):
        # This function simulates accepting payment for a bill.
        # It prints a confirmation message and calls the generate_receipt function.
        print(f"Payment of RM{bill.total_amount:.2f} accepted for customer ID {bill.customer_id}.")
        generate_receipt(bill)


    def generate_receipt(bill):
        # This function generates a receipt for a paid bill and writes it to a file.
        # It creates receipt data, writes it to a file, and thanks the customer for the payment.
        receipt_data = f"\nReceipt:\nCustomer ID: {bill.customer_id}\nTotal Amount: RM{bill.total_amount:.2f}\nThank you for your payment!\n"

        with open("payment_and_receipt.txt", "a") as file:
            file.write(receipt_data)


    def generate_payment_and_receipt(transaction, total_rental_amount):
        # This function simulates generating payment and receipt for a rental transaction.
        # It prints a confirmation message, generates payment date (assuming current date),
        # accepts payment, and generates a receipt.
        payment_date = datetime.datetime.now()

        print(f"Payment of RM{total_rental_amount:.2f} accepted for customer ID {transaction.customer_id}.")

        receipt_data = f"\nReceipt:\nCustomer ID: {transaction.customer_id}\nTotal Amount: RM{total_rental_amount:.2f}\nThank you for your payment!\n"

        with open("payment_and_receipt.txt", "a") as file:
            file.write(receipt_data)


    file_path = 'carinfo.txt'

    customers = []  # List to store customers (Customer objects)
    cars = []  # List to store cars (Car objects)
    rental_transactions = []  # List to store rental transactions

    current_user = None  # Stores currently logged in user
    customer_id_counter = 0  # Initialize the counter
    car_id_counter = 0  # Initialize the counter


    def generate_customer_id():
        # This function generates a unique customer ID by reading the existing customer IDs from the file,
        # finding the maximum ID, incrementing it by 1, and formatting it with leading zeros.
        max_customer_id = 0
        if os.path.exists("customers.txt"):
            with open("customers.txt", "r") as file:
                for line in file:
                    fields = line.strip().split("|")
                    if fields:
                        customer_id_str = fields[0].split(":")[1].strip()[1:]  # Extract customer ID string
                        try:
                            customer_id = int(customer_id_str)
                            max_customer_id = max(max_customer_id, customer_id)
                        except ValueError:
                            pass  # Silently handle the error without printing

        next_customer_id = max_customer_id + 1
        next_customer_id = max(next_customer_id, 1)  # Ensure the next ID is at least 1
        next_customer_id_str = str(next_customer_id).zfill(6)  # Format the ID with leading zeros
        return f"C{next_customer_id_str}"


    def register_customer():
        # This function prompts the user to input customer details, validates the input, generates a unique customer ID,
        # records the registration date, and writes the customer information to a file.
        while True:
            name = input("Enter customer name: ").strip()
            if name:
                break
            else:
                print("Name cannot be blank. Please enter customer name.")

        while True:
            id_type = input("Enter ID type (a for NRIC, b for Passport): ").strip().lower()
            if id_type == "a":
                while True:
                    nric = input("Enter NRIC (should contain only numbers and hyphens): ").strip()
                    if all(c.isdigit() or c == '-' for c in nric):
                        break
                    else:
                        print("Invalid NRIC format. NRIC should contain only numbers and hyphens (-). Please try again.")
                break
            elif id_type == "b":
                passport = input("Enter passport number: ").strip()
                break
            else:
                print("Invalid choice. Please enter 'a' for NRIC or 'b' for Passport.")

        while True:
            phone = input("Enter customer phone number (should contain only numbers and hyphens): ").strip()
            if all(c.isdigit() or c == '-' for c in phone):
                break
            else:
                print("Invalid phone number format. Phone number should contain only numbers and hyphens (-). Please try again.")

        while True:
            license = input("Enter car driving license number: ").strip()
            if license:
                break
            else:
                print("License number cannot be blank. Please enter car driving license number.")

        while True:
            address = input("Enter customer address: ").strip()
            if address:
                break
            else:
                print("Address cannot be blank. Please enter customer address.")

        customer_id = generate_customer_id()
        registration_date = datetime.datetime.now().strftime("%d %B %Y")

        # Writing to customers.txt
        with open("customers.txt", "a") as file:
            if id_type == "a":
                file.write(f"Customer ID: {customer_id} | Name: {name} | NRIC: {nric} | License: {license} | Address: {address} | Phone: {phone} | Registration Date: {registration_date}\n")
            else:
                file.write(f"Customer ID: {customer_id} | Name: {name} | Passport: {passport} | License: {license} | Address: {address} | Phone: {phone} | Registration Date: {registration_date}\n")

        print(f"Customer registered successfully! Customer ID: {customer_id}")
        print("Registration Date:", registration_date)
 

    def load_customers(file_path):
        #This function loads customer data from a specified file path.
        customers = []
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                for line_num, line in enumerate(file, start=1):
                    line = line.replace("|", " | ")  # Add spaces between the field names and the pipes

                    # Extracting customer ID from the line
                    customer_id = line.split("|")[0].split(":")[1].strip()

                    # Split the line by pipes, remove the customer ID, and split the rest using ':'
                    data = [field.split(":")[1].strip() for field in line.split("|")[1:]]

                    if len(data) == 6:  # Ensure each line contains all expected fields
                        # Check if the customer has an NRIC or a Passport
                        if "NRIC" in line:
                            nric = data[1]
                            passport = None
                        else:
                            nric = None
                            passport = data[1]

                        # Creating a Customer object
                        customer = Customer(customer_id, data[0], nric, passport, license=data[2], address=data[3], phone=data[4])
                        customers.append(customer)
                    else:
                        pass
        return customers





    def load_customers_transactions(file_path):
        # This function loads customer data from a file with a different format,
        # creates Customer objects using specific fields, and returns a list of Customer objects.
        customers = []
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) >= 3:  # Ensure at least customer ID, name, and phone are provided
                    customer_id, name, phone = data[:3]  # Extract customer ID, name, and phone
                    # Create a Customer object and append it to the list
                    customers.append(Customer(customer_id, name, phone))
                else:
                    pass
        return customers


    def load_rental_transactions(file_path):
        # This function loads rental transaction data from a file,
        # extracts relevant information, creates RentalTransaction objects,
        # and returns a list of RentalTransaction objects.
        transactions = []
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split(", ")
                if len(data) >= 6:  # Ensure all required fields are provided
                    # Extract relevant information
                    customer_id = None
                    car_reg_number = None
                    rental_date = None
                    return_date = None
                    for item in data:
                        if item.startswith("Customer ID:"):
                            customer_id = item.split(": ")[1]
                        elif item.startswith("Car Registration Number:"):
                            car_reg_number = item.split(": ")[1]
                        elif item.startswith("Rental Date:"):
                            rental_date = datetime.datetime.strptime(item.split(": ")[1], "%d %B %Y").date()
                        elif item.startswith("Return Date:"):
                            return_date = datetime.datetime.strptime(item.split(": ")[1], "%d %B %Y").date()
                    
                    # Check if all required information is available
                    if customer_id and car_reg_number and rental_date and return_date:
                        transaction = RentalTransaction(car_reg_number, customer_id, rental_date, return_date)
                        transactions.append(transaction)
                    else:
                        print("Invalid rental transaction data:", data)
                else:
                    print("Invalid rental transaction data:", data)
        return transactions


    def view_available_cars(file_path):
        # This function allows users to view available cars based on specified preferences.
        # It prompts users to input preferences for car manufacturer, model, year of manufacture,
        # and seating capacity. It then reads car information from a file, filters available cars
        # based on the input preferences, and prints details of available cars.
        manufacturer = input("Enter preferred car manufacturer (leave empty if no preference): ").lower()
        model = input("Enter preferred car model (leave empty if no preference): ").lower()
        year = input("Enter preferred year of manufacture (leave empty if no preference): ").lower()
        
        # Ask for passenger count and validate it
        while True:
            passenger_count = input("Enter preferred seating capacity (4, 7, or 9): ")
            if passenger_count.isdigit():
                passenger_count = int(passenger_count)
                if passenger_count in [4, 7, 9]:
                    break
                else:
                    print("Invalid passenger count. Please choose 4, 7, or 9.")
            else:
                print("Invalid input. Please enter a number.")

        print("\nAvailable Cars:")
        print("{:<25} {:<20} {:<20} {:<10} {:<15}".format("Registration Number", "Manufacturer", "Model", "Year", "Seating Capacity"))

        with open(file_path, 'r') as file:
            for line in file:
                car_data = line.strip().split(', ')
                car_info = {}
                for item in car_data:
                    key, value = item.split(': ')
                    car_info[key.strip()] = value.strip()
                if car_info.get('availability') == 'Available':
                    if (not manufacturer or car_info['carmanufacturer'].lower() == manufacturer) \
                            and (not model or car_info['carmodel'].lower() == model) \
                            and (not year or car_info['yearofmanufacturer'].lower() == year) \
                            and (not passenger_count or int(car_info['seatingcapacity']) == passenger_count):
                        print("{:<25} {:<20} {:<20} {:<10} {:<15}".format(car_info['carregistration'], 
                                                                            car_info['carmanufacturer'], 
                                                                            car_info['carmodel'], 
                                                                            car_info['yearofmanufacturer'],
                                                                            car_info['seatingcapacity']))


    def book_car(customer_id, car_reg_number, rental_date, return_date, file_path):
        # This function handles booking a car for a customer. It checks if the customer exists,
        # finds the car by registration number, checks its availability, calculates rental details,
        # prints rental details, writes rental information to a file, and returns True if the booking is successful.
        with open(file_path, 'r') as file:
            for line in file:
                car_data = line.strip().split(', ')
                car_info = {}
                for item in car_data:
                    key, value = item.split(': ')
                    car_info[key.strip()] = value.strip()

                if car_info['carregistration'] == car_reg_number:
                    if car_info['availability'] == "Available":
                        print("Car booked successfully!")

                        new_rental_transaction = RentalTransaction(car_reg_number, customer_id, rental_date, return_date)

                        rental_periods = (return_date - rental_date).days
                        new_rental_transaction.rental_periods = rental_periods

                        rental_transactions.append(new_rental_transaction)
                        print("Return Date:", return_date.strftime('%d %B %Y'))
                        print("Rental Periods (Days):", rental_periods, "days")
                        
                        # Write booking information to the book_car.txt file
                        with open('book_car.txt', 'a') as book_car_file:
                            book_car_file.write(f"Customer ID: {customer_id}, Car Registration Number: {car_reg_number}, Rental Date: {rental_date.strftime('%d %B %Y')}, Return Date: {return_date.strftime('%d %B %Y')}, Rental Periods (Days): {rental_periods}, Status: Reserved\n")
                        break
                    else:
                        print("Car is not available for rent.")
                        break
            else:
                print("Car not found.")


    def load_car_info(file_path):
        # This function loads car information from a file, creates Car objects for each record,
        # and returns a list of Car objects. It handles the specific format of car data in the file.
        cars = []
        with open(file_path, 'r') as file:
            for line in file:
                car_data = line.strip().split(", ")  # Splitting by ", " instead of just ", "
                if len(car_data) == 12:  # Adjusting the length check based on the actual format
                    reg_number = car_data[0].split(": ")[1]
                    manufacturer = car_data[1].split(": ")[1]
                    model = car_data[2].split(": ")[1]
                    year = car_data[3].split(": ")[1]
                    seating_capacity = car_data[4].split(": ")[1]
                    availability = car_data[9].split(": ")[1]
                    renting_rate = car_data[10].split(": ")[1]
                    cars.append(Car(reg_number, manufacturer, model, int(year), int(seating_capacity), float(renting_rate), availability))
                else:
                    print("Invalid car data:", car_data)
        return cars

    carinfo_file = 'carinfo.txt'

    cars = load_car_info(carinfo_file)
    

    def rent_car(customer_id, car_reg_number, rental_date, return_date, cars, customers):
        # This function facilitates the rental of a car by a customer.
        # It checks if the customer exists, finds the specified car, verifies its availability,
        # calculates rental details, prints rental information, and records the transaction in a file.
        
        customer_found = False
        for customer in customers:
            if customer.customer_id == customer_id:
                customer_found = True
                break

            if not customer_found:
                print("Customer not found.")
                return False

        # Find the car
        car_found = False
        for car in cars:
            if car.reg_number == car_reg_number:
                car_found = True
                if car.status == "Available" or car.status == "Reserved":
                    # Calculate rental periods
                    rental_periods = (return_date - rental_date).days

                    # Get the rental price per day
                    rental_price_per_day = car.rental_price

                    # Calculate total rental
                    total_rental = rental_periods * rental_price_per_day

                    # Format rental date and return date
                    rental_date_str = rental_date.strftime("%d %B %Y")
                    return_date_str = return_date.strftime("%d %B %Y")

                    # Print rental details
                    print("Car rented successfully!")
                    print(f"Rental Date: {rental_date_str}")
                    print(f"Return Date: {return_date_str}")
                    print(f"Rental Periods (Days): {rental_periods} days")
                    print(f"Total Rental: RM{total_rental:.2f}")

                    # Write rental information to the car_rental.txt file
                    with open('car_rental.txt', 'a') as car_rental_file:
                        car_rental_file.write(f"Customer ID: {customer_id}, Car Registration Number: {car_reg_number}, Rental Date: {rental_date_str}, Return Date: {return_date_str}, Rental Periods (Days): {rental_periods}, Total Rental: RM{total_rental:.2f}, Status: Rented\n")

                    return True
                else:
                    print("Car is not available for rent.")
                break

        if not car_found:
            print("Car not found.")

        return False

    customers = load_customers("customers.txt")


    def return_car(car_reg_number, return_date, cars):
        # This function handles the return of a rented car.
        # It finds the car by its registration number and records the return information in a file.
        car_found = False

        # Read car rental information from the "car_rental.txt" file
        if os.path.exists("car_rental.txt"):
            with open("car_rental.txt", "r") as file:
                car_rental_info = file.readlines()

        # Find the car by registration number in the rental records
        for rental_record in car_rental_info:
            if car_reg_number in rental_record:
                car_found = True
                print("Car returned successfully!")
                    
                # Write return information to the return_car.txt file
                with open('return_car.txt', 'a') as return_car_file:
                    return_car_file.write(f"Car Registration Number: {car_reg_number}, Return Date: {return_date}, Status: Available\n")
                break

        if not car_found:
            print("Car not found.")



    def update_car_status(reg_number, new_status, cars):
        # This function updates the status of a car with a specified registration number.
        # It modifies the status of the car object in the list of cars and updates the status
        # in the car information file.
        for car in cars:
            if car.reg_number == reg_number:
                car.status = new_status
                print(f"Status of car with registration number {reg_number} updated to {new_status}.")
                break
        else:
            print(f"Car with registration number {reg_number} not found.")

        # Update car status in the file
        with open('carinfo.txt', 'r') as file:
            lines = file.readlines()

        updated_lines = []
        for line in lines:
            if reg_number in line:
                line = line.replace('availability: Available', f'availability: {new_status}')
            updated_lines.append(line)

        with open('carinfo.txt', 'w') as file:
            file.writelines(updated_lines)
            file.close()

    def car_info(file_path):
        # This function displays information about all cars, including their registration number,
        # manufacturer, model, year of manufacture, seating capacity, and availability status.
        # It reads car information from a file and prints details for each car.
        print("\nAll Car Information and Status:")
        with open(file_path, 'r') as file:
            for line in file:
                car_data = line.strip().split(', ')
                car_info = {}
                for item in car_data:
                    key, value = item.split(': ')
                    car_info[key.strip()] = value.strip()
                print("Registration Number:", car_info['carregistration'])
                print("Manufacturer:", car_info['carmanufacturer'])
                print("Model:", car_info['carmodel'])
                print("Year:", car_info['yearofmanufacturer'])
                print("Seating Capacity:", car_info['seatingcapacity'])
                print("Car Status:", car_info['availability'])
                print()  # Empty line for better readability


    def view_rental_transactions(date):
        # This function displays rental transactions that occurred on a specified date.
        # It reads transaction data from the 'car_rental.txt' file, filters transactions
        # based on the specified date, and prints relevant information about each transaction.
        rental_transactions_on_date = []
        with open('car_rental.txt', 'r') as file:
            for line in file:
                transaction_data = line.strip().split(', ')
                transaction_info = {}
                for item in transaction_data:
                    key, value = item.split(': ')
                    transaction_info[key.strip()] = value.strip()

                # Parse dates from string to datetime
                rental_date = datetime.datetime.strptime(transaction_info['Rental Date'], "%d %B %Y").date()
                return_date = datetime.datetime.strptime(transaction_info['Return Date'], "%d %B %Y").date()

                # Check if the transaction falls on the specified date
                if rental_date == date.date():
                    # Create a RentalTransaction object using data from file
                    rental_transaction = RentalTransaction(transaction_info['Car Registration Number'],
                                                           transaction_info['Customer ID'],
                                                           rental_date,
                                                           return_date,
                                                           float(transaction_info['Total Rental'].replace('RM', '')))
                    rental_transactions_on_date.append(rental_transaction)

        if not rental_transactions_on_date:
            print("No rental transactions found for the specified date.")
            return

        print("Rental Transactions on", date.strftime("%d %B %Y"))
        for transaction in rental_transactions_on_date:
            print("Car Registration Number:", transaction.car_reg_number)
            print("Customer ID:", transaction.customer_id)
            print("Rental Date:", transaction.rental_date.strftime("%d %B %Y"))
            print("Return Date:", transaction.return_date.strftime("%d %B %Y"))
            print("Rental Periods (Days):", transaction.rental_periods)
            # Print the total rental amount for each transaction
            print("Total Rental: RM{:.2f}".format(transaction.total_rental))
            print()  # Print an empty line for better readability


    def delete_cancelled_rental_transaction(car_reg_number):
        # This function deletes a rental transaction associated with a specific car registration number.
        # It removes the transaction from the 'car_rental.txt' file and updates the global list
        # of rental_transactions accordingly.
        global rental_transactions
        
        # Read all rental transactions from the car_rental.txt file
        with open('car_rental.txt', 'r') as file:
            lines = file.readlines()

        # Filter out the transactions with the specified car registration number
        updated_lines = [line for line in lines if car_reg_number not in line]

        # Write the filtered transactions back to the car_rental.txt file
        with open('car_rental.txt', 'w') as file:
            file.writelines(updated_lines)

        # Update the rental_transactions list by filtering out the deleted transactions
        rental_transactions = [transaction for transaction in rental_transactions if transaction.car_reg_number != car_reg_number]

        print("Cancelled rental transactions deleted successfully.")


    def update_customer_details(customer_id):
        global customers  # Use the global customers list

        # Read customers from customers.txt
        customers = []
        with open("customers.txt", "r") as file:
            for line in file:
                customer_info = line.strip().split(" | ") # Split line by delimiter " | "
                customer_id = customer_info[0].split(": ")[1]
                name = customer_info[1].split(": ")[1]
                id_type = "nric" if "NRIC" in customer_info[2] else "passport"
                id_number = customer_info[2].split(": ")[1]
                license = customer_info[3].split(": ")[1]
                address = customer_info[4].split(": ")[1]
                phone = customer_info[5].split(": ")[1]
                registration_date = customer_info[6].split(": ")[1]
                # Create Customer object based on ID type
                if id_type == "nric":
                    customer = Customer(customer_id, name, id_number, license, address, phone, registration_date)
                else:
                    customer = Customer(customer_id, name, "", license, address, phone, registration_date, passport=id_number)

                customers.append(customer)

        # Strip any extra whitespace from the input customer_id
        customer_id = customer_id.strip()

        for customer in customers:
            # Extracting customer ID from the customer object without any prefix
            extracted_customer_id = customer.customer_id.strip()

            # Comparing the extracted customer ID with the user input
            if extracted_customer_id == customer_id:
                print(f"Customer details for {customer.name} (Customer ID: {extracted_customer_id})")
                
                available_fields = {"a": "phone", "b": "address", "c": "license", "d": "passport"}
                allowed_choices = ["a", "b", "c", "d"]
                
                fields_to_update = input("Enter fields to update (a: phone, b: address, c: license, d: passport), separated by commas: ")
                fields = fields_to_update.strip().lower().split(",")
                
                update_successful = False
                
                for field in fields:
                    field = field.strip()
                    if field in allowed_choices:
                        if available_fields[field] == "phone":
                            new_phone = input("Enter new phone number: ")
                            if all(char.isdigit() or char == '-' for char in new_phone):
                                customer.phone = new_phone
                                update_successful = True
                            else:
                                print("Invalid phone number format. Please use only numbers and hyphens.")
                        elif available_fields[field] == "address":
                            customer.address = input("Enter new address: ")
                            update_successful = True
                        elif available_fields[field] == "license":
                            customer.license = input("Enter new license number: ")
                            update_successful = True
                        elif available_fields[field] == "passport":
                            if customer.nric:
                                print("NRIC customer cannot update passport.")
                            else:
                                customer.passport = input("Enter new passport number: ")
                                update_successful = True
                    else:
                        print(f"Invalid field: {field}")
                
                if update_successful:
                    print("Customer details updated successfully!")
                    # Update the customers.txt file with the updated details
                    with open("customers.txt", "w") as file:
                        for cust in customers:
                            # Write each customer's details in the specified format
                            if cust.nric:
                                file.write(f"Customer ID: {cust.customer_id} | Name: {cust.name} | NRIC: {cust.nric} | License: {cust.license} | Address: {cust.address} | Phone: {cust.phone} | Registration Date: {cust.registration_date}\n")
                            else:
                                file.write(f"Customer ID: {cust.customer_id} | Name: {cust.name} | Passport: {cust.passport} | License: {cust.license} | Address: {cust.address} | Phone: {cust.phone} | Registration Date: {cust.registration_date}\n")
                    return
            else:
                print("Customer not found!")



    def view_customers(file_path):
        # Load customer details from the file
        customers = load_customers(file_path)

        # Check if there are any customers registered
        if not customers:
            print("No customers registered yet!")
            return

        # Print the details of each customer in a formatted table
        print("{:<20} {:<30} {:<20} {:<20} {:<30} {:<20} {:<20}".format("Customer ID", "Name", "NRIC/Passport", "License", "Address", "Phone", "Registration Date"))
        for customer in customers:
            print("{:<20} {:<30} {:<20} {:<20} {:<30} {:<20} {:<20}".format(customer.customer_id, customer.name, customer.nric or customer.passport, customer.license, customer.address, customer.phone, customer.registration_date))


    def update_profile(file_path):
        global current_user # Use the global current_user variable

        # Check if the profile file exists and is not empty
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, "r") as file:  # Open the file in read mode
                line = file.readline().strip()  # Read the first line and strip any leading/trailing whitespace
                if line:
                    data = [field.split(":")[1].strip() for field in line.split("|")]
                    if len(data) == 5:  # Check if the line contains all expected fields
                        current_user = UserProfile(*data)  # Create a UserProfile object with extracted data
                    else:
                        print("Invalid data format in profile file.")
                        return
        else:
            print("Please enter your details.")
            # Prompt user to enter their details
            name = input("Enter your name: ")
            phone_number = input("Enter your phone number: ")
            address = input("Enter your address: ")
            email = input("Enter your email: ")
            job_title = input("Enter your job title: ")
            
            current_user = UserProfile(name, phone_number, address, email, job_title)

            # Save the new profile to the file
            with open(file_path, "w") as file:
                file.write(str(current_user) + "\n")
            
            print(f"Profile created successfully for {current_user.name}!")
            return

        print(f"Current profile details:\n{current_user}")

        print("\nUpdate Options:")
        print("a. Name")
        print("b. Phone Number")
        print("c. Address")
        print("d. Email")
        print("e. Job Title")

        available_fields = {"a": "name", "b": "phone_number", "c": "address", "d": "email", "e": "job_title"}
        allowed_choices = ["a", "b", "c", "d", "e"]
        # Prompt user for fields to update
        fields_to_update = input("Enter fields to update (a: name, b: phone number, c: address, d: email, e: job title), separated by commas: ")
        fields = fields_to_update.strip().lower().split(",")

        update_successful = False  # Flag to track if any update was successful

        for field in fields:  # Loop through each field to update
            field = field.strip()
            if field in allowed_choices:  # Check if the field is allowed
                if available_fields[field] == "name":  # Name
                    new_name = input("Enter new name: ")
                    current_user.name = new_name
                    update_successful = True
                elif available_fields[field] == "phone_number":  # Phone Number
                    new_phone_number = input("Enter new phone number: ")
                    if all(char.isdigit() or char == '-' for char in new_phone_number):
                        current_user.phone_number = new_phone_number
                        update_successful = True
                    else:
                        print("Invalid phone number format. Please use only numbers and hyphens.")
                elif available_fields[field] == "address":  # Address
                    new_address = input("Enter new address: ")
                    current_user.address = new_address
                    update_successful = True
                elif available_fields[field] == "email":  # Email
                    new_email = input("Enter new email: ")
                    current_user.email = new_email
                    update_successful = True
                elif available_fields[field] == "job_title":  # Job Title
                    new_job_title = input("Enter new job title: ")
                    current_user.job_title = new_job_title
                    update_successful = True
            else:
                print(f"Invalid field: {field}")

        if update_successful:
            print("Profile updated successfully!")
            print("Updated Profile:")
            print(f"Name: {current_user.name}")
            print(f"Phone Number: {current_user.phone_number}")
            print(f"Address: {current_user.address}")
            print(f"Email: {current_user.email}")
            print(f"Job Title: {current_user.job_title}")

            # Write user profile back to file
            with open(file_path, "w") as file:  # Open the file in write mode
                file.write(str(current_user) + "\n") # Write updated user profile to the file
        else:
            print("No fields were updated.")


    def delete_customer(customer_id):
        # Read customers from file
        customers = load_customers("customers.txt")

        # Delete customer
        for idx, customer in enumerate(customers):  # Iterate over the list of customers
            if customer.customer_id.strip() == customer_id.strip():  # Check if the current customer ID matches the input ID
                del customers[idx]  # Delete the customer from the list
                print(f"Customer with ID {customer_id} deleted successfully!")
                break
        else:
            print("Customer ID not found!")
            return

        # Update customer IDs and rewrite the customers.txt file
        for i, cust in enumerate(customers, start=1):  # Re-assign customer IDs to maintain sequence
            cust.customer_id = f"C{i:06d}"  # Format the new customer ID with leading zeros
        with open("customers.txt", "w") as file:
            for cust in customers:   # Iterate over the updated list of customers
                if hasattr(cust, 'nric'):  # Check if the customer has an NRIC attribute
                    file.write(f"Customer ID: {cust.customer_id} | Name: {cust.name} | NRIC: {cust.nric} | License: {cust.license} | Address: {cust.address} | Phone: {cust.phone} | Registration Date: {cust.registration_date}\n")
                else:
                    file.write(f"Customer ID: {cust.customer_id} | Name: {cust.name} | Passport: {cust.passport} | License: {cust.license} | Address: {cust.address} | Phone: {cust.phone} | Registration Date: {cust.registration_date}\n")

    class UserProfile:
        # This class represents a user profile with attributes such as name, phone number, address, email, and job title.
        # It provides a convenient way to store and manage user profile information.
        def __init__(self, name, phone_number=None, address=None, email=None, job_title=None):
            self.name = name
            self.phone_number = phone_number
            self.address = address
            self.email = email
            self.job_title = job_title
        def __str__(self):
            return f"Name: {self.name} | Phone Number: {self.phone_number} | Address: {self.address} | Email: {self.email} | Job Title: {self.job_title}"

    def user_name():
        # This function prompts the user to enter their name and initializes the current_user UserProfile object.
        # It welcomes the user with their name and prepares to manage their profile.
        global current_user
        name = input("Enter your name: ")
        current_user = UserProfile(name)
        print(f"Welcome {current_user.name}!")


    def main_menu():
        # This function displays the main menu options and handles user input to navigate to different menu choices.
        while True:
            print("\nMain Menu:")
            print("1. Customer Service Staff I Menu")
            print("2. Customer Service Staff II Menu")
            print("3. Logout")
            choice = input("\nEnter your choice (1-3): ")
            if choice == '1':
                menu_1()  # Enter Customer Service Staff I Menu
            elif choice == '2':
                menu_2(carinfo_file)  # Enter Customer Service Staff II Menu
            elif choice == '3':
                logout()
                break
            else:
                print("Invalid choice. Please try again.")


    def menu_1():
        # This function displays the Customer Service Staff I menu options and handles user input accordingly.
        # It allows staff to register customers, update customer details, view customer information,
        # update their own profile, and delete customer records.
        global customers  # Ensure we're using the global 'customers' variable
        # Load existing customers
        customers = load_customers("customers.txt")
        profile_file_path = "customer_staff_profile.txt"
        while True:
            print("\nCustomer Service Staff I Menu")
            print("1. Register Customer")
            print("2. Update Customer Details")
            print("3. View Customers")
            print("4. Update Profile")
            print("5. Delete Customer")
            print("6. Back to Main Menu")
            choice_staff = input("\nEnter your choice (1-6): ")
            if choice_staff not in ('1', '2', '3', '4', '5', '6'):
                print("Invalid choice. Please try again.")
                continue
            if choice_staff == '1':
                register_customer()
            elif choice_staff == '2':
                customer_id = input("Enter customer ID to update: ")
                update_customer_details(customer_id)
            elif choice_staff == '3':
                view_customers("customers.txt")
            elif choice_staff == '4':
                update_profile(profile_file_path)
            elif choice_staff == '5':
                customer_id = input("Enter customer ID: ")
                delete_customer(customer_id)
            elif choice_staff == '6':
                break  # Exit Customer Service Staff I Menu


    cars = load_car_info(carinfo_file)

    customers = load_customers("customers.txt")


    def menu_2(file_path):
        # This function displays the Customer Service Staff II menu options and handles user input accordingly.
        # It allows staff to perform various actions related to car rental management, such as viewing available cars,
        # booking cars, renting cars, returning cars, generating bills, managing payments and receipts,
        # updating rental availability, viewing rental transactions, and deleting cancelled rental transactions.
        global cars
        global customers
        while True:
            print("\nCustomer Service Staff II Menu")
            print("1. View Available Cars")
            print("2. Book Car")
            print("3. Rent Car")
            print("4. Return Car")
            print("5. Generate Bill")
            print("6. Payment and Receipt")
            print("7. Update Rental Availability")
            print("8. View List Of Rental Transactions")
            print("9. Delete Cancelled Rental Transaction")
            print("10. Back to Main Menu")
            choice_staff = input("\nEnter your choice (1-10): ")
            if choice_staff not in ('1', '2', '3', '4', '5', '6', '7', '8', '9','10'):
                print("Invalid choice. Please try again.")
                continue
            if choice_staff == '1':
                view_available_cars('carinfo.txt')
            elif choice_staff == '2':
                while True:
                    customer_id = input("Enter customer ID: ")
                    car_reg_number = input("Enter car registration number: ")
                    rental_date_str = input("Enter rental date (DD Month YYYY): ")
                    return_date_str = input("Enter return date (DD Month YYYY): ")

                    try:
                        # Convert rental and return date strings to datetime objects
                        rental_date = datetime.datetime.strptime(rental_date_str, "%d %B %Y")
                        return_date = datetime.datetime.strptime(return_date_str, "%d %B %Y")
                        break  # Exit the loop if conversion is successful
                    except ValueError:
                        print("Invalid date format. Please use DD Month YYYY (e.g., 03 February 2024).")

                # Call the book_car function with the provided inputs
                book_car(customer_id, car_reg_number, rental_date, return_date, file_path)
            elif choice_staff == '3':
                while True:
                    customer_id = input("Enter customer ID: ")
                    car_reg_number = input("Enter car registration number: ")
                    rental_date_str = input("Enter rental date (DD Month YYYY): ")
                    return_date_str = input("Enter return date (DD Month YYYY): ")

                    try:
                        # Convert rental and return date strings to datetime objects
                        rental_date = datetime.datetime.strptime(rental_date_str, "%d %B %Y")
                        return_date = datetime.datetime.strptime(return_date_str, "%d %B %Y")

                        # Call the rent_car function with the provided inputs
                        rent_car(customer_id, car_reg_number, rental_date, return_date, cars, customers)
                        break  # Exit the loop after successfully renting the car
                    except ValueError:
                        print("Invalid date format. Please use DD Month YYYY (e.g., 03 February 2024).")

            elif choice_staff == '4':
                car_reg_number = input("Enter car registration number: ")
                return_date_str = input("Enter return date (DD Month YYYY): ")
                try:
                    return_date = datetime.datetime.strptime(return_date_str, "%d %B %Y").date()
                    return_car(car_reg_number, return_date, cars)
                except ValueError:
                    print("Invalid date format. Please use DD Month YYYY (e.g., 03 February 2024).")

            elif choice_staff == '5':
                file_path_customers = 'customers.txt'  # Path to the customers file
                file_path_rentals = 'car_rental.txt'   # Path to the rental transactions file
                customer_id = input("Enter customer ID: ")
                
                # Load customer data
                customers = load_customers_transactions(file_path_customers)
                
                # Load rental transactions
                rental_transactions = load_rental_transactions(file_path_rentals)
                
                # Find the rental transaction associated with the customer ID
                rental_transaction = None
                for transaction in rental_transactions:
                    if transaction.customer_id == customer_id:
                        rental_transaction = transaction
                        break
                
                if rental_transaction:
                    # Create a new transaction object using the rental transaction data
                    generate_bill(rental_transaction, file_path_rentals)
                else:
                    print("No rental transaction found for the entered customer ID.")

            elif choice_staff == '6':
                customer_id = input("Enter customer ID: ")
                # Load rental transactions
                file_path_rentals = 'car_rental.txt'
                rental_transactions = load_rental_transactions(file_path_rentals)

                # Find the rental transactions associated with the customer ID
                transactions = [transaction for transaction in rental_transactions if transaction.customer_id == customer_id]
                if not transactions:
                    print("No rental transactions found for the entered customer ID.")
                else:
                    print("\nRental Transactions:")
                    for transaction in transactions:
                        rental_date_formatted = transaction.rental_date.strftime("%d %B %Y")
                        return_date_formatted = transaction.return_date.strftime("%d %B %Y")
                        print("Car Registration Number:", transaction.car_reg_number)
                        print("Rental Date:", rental_date_formatted)
                        print("Return Date:", return_date_formatted)
                        print("Rental Periods (Days):", transaction.rental_periods)
                        # Generate bill and receipt for each transaction
                        bill = generate_bill(transaction, file_path_rentals)  # Generate the bill
                        if bill:  # If bill is generated successfully
                            total_rental_amount = bill.total_amount  # Extract total_rental_amount
                            print(f"Total Rental: RM{total_rental_amount:.2f}")
                            generate_payment_and_receipt(transaction, total_rental_amount)  # Generate payment and receipt
                    print("Receipt generation completed.")

            elif choice_staff == '7':
                reg_number = input("Enter car registration number: ")
                new_status = input("Enter new status (Available, Reserved, or Rented): ").capitalize()
                
                if new_status not in ['Available', 'Reserved', 'Rented']:
                    print("Invalid status. Please enter Available, Reserved, or Rented.")
                else:
                    update_car_status(reg_number, new_status, cars)
                    car_info(file_path)
            elif choice_staff == '8':
                while True:
                    try:
                        date_str = input("Enter date to view rental transactions (DD Month YYYY): ")
                        date = datetime.datetime.strptime(date_str, "%d %B %Y")
                        break  # Exit the loop if parsing is successful
                    except ValueError:
                        print("Invalid date format. Please use DD Month YYYY (e.g., 03 February 2024).")
                view_rental_transactions(date)
            elif choice_staff == '9':
                car_reg_number = input("Enter car registration number: ")
                delete_cancelled_rental_transaction(car_reg_number)
            elif choice_staff == '10':
                break  # Exit Customer Service Staff II Menu


    def logout():
        # This function logs out the current user by setting the current_user variable to None and prints a logout message.
        global current_user
        current_user = None
        print("Logged out successfully!")


    # Main program
    # The user_name function prompts the user to enter their name and initializes the current_user UserProfile object.
    # Then, the main_menu function is called to start the main menu interface.
    user_name()
    main_menu()