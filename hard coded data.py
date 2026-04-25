# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 18:06:09 2024

@author: User
"""


# Define the lists and manager dictionary
# Hard-coded data
customer_staff_1_list = [{'username': 'Ian', 'name': 'Ian Lim', 'password': '1234', 'role': 'Customer Service Staff', 'registerdate': '16-04-2024', 'age': '19', 'DOB': '22 08 2005', 'contact information': '0126420822', 'gender': 'Male'}]

car_service_staff_list = [{'username': 'Chan', 'name': 'Chan kar jun', 'password': '1234', 'role': 'Car Service Staff', 'registerdate': '16-04-2024', 'age': '19', 'DOB': '22 08 2005', 'contact information': '0126420822', 'gender': 'Male'}]
manager = [{'username': 'Hermen', 'name': 'Ang Kuan Hern', 'password': '1234', 'role': 'Manager', 'registerdate': '16-04-2024', 'age': '19', 'DOB': '22 08 2005', 'contact information': '0126420822', 'gender': 'Male'}]

# File paths
customer_staff_1_file = 'customer_staff.txt'

car_service_staff_file = 'car_service_staff.txt'
manager_file = 'manager.txt'
car_renting_rates_file = 'car_renting_rates.txt'

# Function to write data to file
def write_data_to_file(data, file_path):
    with open(file_path, 'w') as file:
        for item in data:
            file.write(str(item) + '\n')  # Write each dictionary as a string followed by a newline

def append_unique_data_to_file(data, file_path):
    with open(file_path, 'r+') as file:
        existing_data = file.read()
        for item in data:
            formatted_item = ', '.join([f"{key}: {value}" for key, value in item.items()])
            if formatted_item + '\n' not in existing_data:
                file.write(formatted_item + '\n')

# Append the unique hard-coded data to the files
append_unique_data_to_file(customer_staff_1_list, customer_staff_1_file)

append_unique_data_to_file(car_service_staff_list, car_service_staff_file)
append_unique_data_to_file(manager, manager_file)
# Function to write data to file

carinfo = [{'carregistration': 'BNL2778','carmanufacturer':'Honda', 'carmodel': 'Accord','yearofmanufacturer': '2015','seatingcapacity': '4','lastservicedate': '22 08 2005','insurancepolicynumber': 'XA123456','insuranceexpirydate': '22 08 2005','roadtaxexpirydate':'22 08 2005','availability':'Available','car renting rate':'200','returndate': None},
           {'carregistration': 'BNL1346','carmanufacturer':'Honda', 'carmodel': 'Accord','yearofmanufacturer': '2015','seatingcapacity': '4','lastservicedate': '22 08 2005','insurancepolicynumber': 'XA123456','insuranceexpirydate': '22 08 2005','roadtaxexpirydate':'22 08 2005','availability':'Disposed','car renting rate':'200','returndate': None},
           {'carregistration': 'BNL8765','carmanufacturer':'Honda', 'carmodel': 'Accord','yearofmanufacturer': '2015','seatingcapacity': '4','lastservicedate': '22 08 2005','insurancepolicynumber': 'XA123456','insuranceexpirydate': '22 08 2005','roadtaxexpirydate':'22 08 2005','availability':'Rented','car renting rate':'200','returndate': '11 11 2005'},
           {'carregistration': 'BNL4783','carmanufacturer':'Honda', 'carmodel': 'Accord','yearofmanufacturer': '2015','seatingcapacity': '4','lastservicedate': '22 08 2005','insurancepolicynumber': 'XA123456','insuranceexpirydate': '22 08 2005','roadtaxexpirydate':'22 08 2005','availability':'Reserved','car renting rate':'200','returndate': None},
           {'carregistration': 'BNL7584','carmanufacturer':'Honda', 'carmodel': 'Accord','yearofmanufacturer': '2015','seatingcapacity': '4','lastservicedate': '22 08 2005','insurancepolicynumber': 'XA123456','insuranceexpirydate': '22 08 2005','roadtaxexpirydate':'22 08 2005','availability':'Under Service','car renting rate':'200','returndate': None}]
carinfo_file = 'carinfo.txt'
append_unique_data_to_file(carinfo, carinfo_file)