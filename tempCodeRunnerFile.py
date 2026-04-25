def update_customer_details(customer_id):
        # This function allows updating details of a customer with a specified ID.
        # It prompts the user to select which fields to update (phone, address, license, or passport),
        # and then modifies the corresponding customer object. It also updates the 'customers.txt' file
        # with the new customer details.
        global customers  # Use the global customers list
        customers = load_customers("customers.txt")
    
        # Debug: Print the list of loaded customers
        print(f"Loaded customers: {len(customers)}")
        for customer in customers:
            print(customer)
        
        for customer in customers:
            if customer.customer_id.strip() == customer_id.strip():
                print(f"Customer details for {customer.name} (ID: {customer_id})")
                
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
                            file.write(f"{cust.customer_id},{cust.name},{cust.nric},{cust.passport},{cust.license},{cust.address},{cust.phone}\n")
                    return
        print("Customer not found!")