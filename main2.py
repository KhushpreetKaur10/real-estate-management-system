import os
import re
from datetime import datetime
from getpass import getpass

properties=[]
clients=[]
clientBookings = [] 
ADMINpassword='1234'

if not os.path.exists("data"):
    os.makedirs("data")


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10



def writePropDataToFile():
    if not os.path.exists('data/ALLproperties.txt'):
        open('data/ALLproperties.txt', 'w').close()
    print("\nEnter the following details to add a property record-\n")
    id = input("ID: ")
    exists = False
    with open('data/ALLproperties.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(";")
            if parts and parts[0].strip() == id:
                exists = True
                break
    if not exists:
        loc = input("Location: ")
        type = input("Type: ")
        price = input("Price: ")
        status = 'Available'
        with open('data/ALLproperties.txt', 'a') as f:
            line = f"{id} ; {loc} ; {type} ; {price} ; {status}\n"
            f.write(line)
            print("Property details added successfully.")
    else:
        print("❗ This property ID already exists.")


def readPropFileStoreList():
    global properties
    properties = []
    with open('data/ALLproperties.txt', 'r') as f:
        for line in f:
            id, loc, type, price, status = line.strip().split(";")
            properties.append({
                'ID': id,
                'Location': loc,
                'Type': type,
                'Price': price,
                'Status': status
            })
    return properties


# auto incremented id
def get_next_id(filename='data/ALLclients.txt'):
    max_id = 0
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split(';')
                if parts and parts[0].strip().isdigit():
                    current_id = int(parts[0].strip())
                    if current_id > max_id:
                        max_id = current_id
    return max_id + 1


def writeClientsData():
    client_file = 'data/ALLclients.txt'
    print("\nADD A CLIENT -")
    name = input("Name: ")
    city = input("City: ")
    while True:
        phone = input("Phone number: ")
        if is_valid_phone(phone):
            break
        else:
            print("❌ Invalid phone number. Must be 10 digits.")
    while True:
        email = input("Email: ")
        if is_valid_email(email):
            break
        else:
            print("❌ Invalid email format. Please try again.")
    # Check duplicates directly from file
    if os.path.exists(client_file):
        with open(client_file, 'r') as f:
            for line in f:
                parts = [p.strip() for p in line.strip().split(';')]
                if len(parts) >= 5:
                    existing_phone = parts[3]
                    existing_email = parts[4]
                    if phone == existing_phone or email == existing_email:
                        print("⚠️ : Client is already registered.\n")
                        return -1
    while True:
        password = getpass("Set Password: ")
        confirmpass = getpass("Confirm password: ")
        if password == confirmpass:
            new_id = get_next_id(client_file)
            with open(client_file, 'a') as f:
                line = f"{new_id} ; {name} ; {city} ; {phone} ; {email} ; {password}\n"
                f.write(line)
            print("✅ Client registered successfully.\n")
            break
        else:
            print("⚠️ : Password didn't match. Try again.")


def readClientFileStoreList():
    global clients
    clients = []
    with open('data/ALLclients.txt', 'r') as f:
        for line in f:
            id, name, city, phone, email, password = line.strip().split(";")
            clients.append({
                'ID': id,
                'Name': name,
                'City': city,
                'Phone Number': phone,
                'Email': email,
                'Password': password
            })
    return clients






def welcomeScreen():
    print("\n\n🏘️  Welcome to Python Real Estate Portal 🏘️\n")

def adminMenu():
    print("\n--------------------------------------------------")
    print("MENU:")
    print("1. View all properties")
    print("2. Search by location")
    print("3. Search by type")
    print("4. Search by price range")
    print("5. View property details")
    print("6. Book a property")
    print("7. Cancel booking")
    print("8. Compare two properties")
    print("9. Suggest properties within budget")
    print("10. Sort properties")
    print("11. Add property record")
    print("12. Delete property record")
    print("13. View Clients")
    print("14. View Client Bookings")
    print("15. Add client")
    print("16. Remove client")
    print("17. Change Password")
    print("18. Exit")
    print("--------------------------------------------------")

def guestMenu():
    print("\n--------------------------------------------------")
    print("MENU:")
    print("1. View all properties")
    print("2. Search by location")
    print("3. Search by type")
    print("4. Search by price range")
    print("5. View property details")
    print("6. Compare two properties")
    print("7. Suggest properties within budget")
    print("8. Sort properties")
    print("9. Exit")
    print("--------------------------------------------------")

def clientMenu():
    print("\n--------------------------------------------------")
    print("MENU:")
    print("1. View all properties")
    print("2. Search by location")
    print("3. Search by type")
    print("4. Search by price range")
    print("5. View property details")
    print("6. Book a property")
    print("7. Cancel booking")
    print("8. Compare two properties")
    print("9. Suggest properties within budget")
    print("10. Sort properties")
    print("11. Change Password")
    print("12. Exit")
    print("--------------------------------------------------")


def viewProp():
    print("\nAll properties: \n")
    print("------------------------------------------------------------------------------------------------")
    print("{:<10} {:<15} {:<15} {:<15} {:<15}".format("ID", "Location", "Type", "Price(in Rs)", "Status"))
    print("------------------------------------------------------------------------------------------------")
    for prop in properties:
        if prop['Status'].lower().strip().startswith('booked by '):
            prop['Status']=' Booked'
        print("{:<10} {:<15} {:<15} {:<15} {:<15}".format(prop['ID'], prop['Location'], prop['Type'], prop['Price'], prop['Status']))
    print("------------------------------------------------------------------------------------------------")


def searchByLoc():
    loc=input("\nEnter the location to search🔍: ").strip().lower()
    locFound=[]
    for prop in properties:
        if loc == prop['Location'].strip().lower():
            locFound.append(prop)
    if locFound:
        print(f"Search results for '{loc}':\n")
        print("{:<10} {:<15} {:<15} {:<15} {:<15}".format("ID", "Location", "Type", "Price(in Rs)", "Status"))
        print("------------------------------------------------------------------------------------------------")
        for locProp in locFound:
            if locProp['Status'].lower().strip().startswith('booked by '):
                locProp['Status']=' Booked'
            print("{:<10} {:<15} {:<15} {:<15} {:<15}".format(locProp['ID'], locProp['Location'], locProp['Type'], locProp['Price'], locProp['Status']))
        print("------------------------------------------------------------------------------------------------")
    else:
        print("⚠️ : No such location found.")





def searchByType():
    unique_types = {prop['Type'] for prop in properties}
    if not unique_types:
        print("⚠️ : No properties available.")
        return
    print("\nAvailable property types:")
    for t in unique_types:
        print(f"🔸 {t}")
    typeInput=input("\nEnter the type to search🔍: ").strip().lower()
    typeFound=[]
    for prop in properties:
        if typeInput == prop['Type'].strip().lower():
            typeFound.append(prop)
    if typeFound:
        print(f"{typeInput} found:\n")
        print("{:<10} {:<15} {:<15} {:<15} {:<15}".format("ID", "Location", "Type", "Price(in Rs)", "Status"))
        print("------------------------------------------------------------------------------------------------")
        for typeProp in typeFound:
            if typeProp['Status'].lower().strip().startswith('booked by '):
                typeProp['Status']=' Booked'
            print("{:<10} {:<15} {:<15} {:<15} {:<15}".format(typeProp['ID'], typeProp['Location'], typeProp['Type'], typeProp['Price'], typeProp['Status']))
        print("------------------------------------------------------------------------------------------------")
    else:
        print("⚠️ : No such type found.")


def searchByPrice():
    print("\nWhat is your price range to search? ")
    minPrice=input("Minimum price: ").replace(",", "")
    maxPrice=input("Maximum price: ").replace(",", "")
    priceFound=[]
    for prop in properties:
        propPrice = int(prop['Price'].replace(",", ""))
        if propPrice >= int(minPrice) and propPrice <= int(maxPrice):
            priceFound.append(prop)
    if priceFound:
        print(f"Properties between Rs.{minPrice} and Rs.{maxPrice} :\n")
        print("{:<10} {:<15} {:<15} {:<15} {:<15}".format("ID", "Location", "Type", "Price(in Rs)", "Status"))
        print("------------------------------------------------------------------------------------------------")
        for locProp in priceFound:
            if locProp['Status'].lower().strip().startswith('booked by '):
                locProp['Status']=' Booked'
            print("{:<10} {:<15} {:<15} {:<15} {:<15}".format(locProp['ID'], locProp['Location'], locProp['Type'], locProp['Price'], locProp['Status']))
        print("------------------------------------------------------------------------------------------------")
    else:
        print("⚠️ : No such properties with this price range Found\n")


def viewPropDetails():
    inputID=input("\nEnter property ID: ").strip()
    found = False
    for prop in properties:
        if inputID == prop['ID'].strip():
            # print(f"Property with ID {inputID} found.")
            print("\nProperty Details:")
            print("-" * 40)
            for key, value in prop.items():
                if prop['Status'].lower().strip().startswith('booked by '):
                    prop['Status']=' Booked'
                print(f"{key}: {value}")
            found=True
    if found != True:
        print(f"⚠️ : No such property with ID {inputID} found.")


def sortPropByPrice():
    if not properties:
        print("⚠️ No properties available to sort.")
        return
    while True:
        user_input = input(f"How many top properties do you want to sort?(max {len(properties)}): ")
        if not user_input.isdigit():
            print("❌ Invalid input. Please enter a numeric value.")
            continue
        sortNo = int(user_input)
        if 1 < sortNo <= len(properties):
            break
        else:
            print(f"⚠️ Please enter a number between 2 and {len(properties)}.")
    #descending order
    top_props = sorted(properties, key=lambda x: int(x['Price'].replace(",", "")), reverse=True)[:sortNo]
    #horizontal bar graph
    print(f"\n💰 Top {user_input} properties: \n")
    max_price = int(top_props[0]['Price'].replace(",", ""))
    scale = max_price / 50  # Max width = 50 chars
    for prop in top_props:
        price = int(prop['Price'].replace(",", ""))
        bar = '🟥' * int(price / scale)
        print(f"{prop['ID']:<5} | {bar} ₹{prop['Price']}")
        print("➖"* (int(price / scale)+11))


def compareProp():
    try:
        id1 = input("\nEnter the first property ID to compare: ").strip()
        id2 = input("Enter the second property ID to compare: ").strip()
        prop1 = None
        prop2 = None
        for prop in properties:
            if id1 == prop['ID'].strip():
                prop1 = prop
            if id2 == prop['ID'].strip():
                prop2 = prop
        if not prop1 or not prop2:
            print("One or both property IDs not found.")
            return
        if prop1['Status'].lower().strip().startswith('booked by '):
            prop1['Status'] = ' Booked'
        if prop2['Status'].lower().strip().startswith('booked by '):
            prop2['Status'] = ' Booked'
        print("\nComparing Properties:\n")
        print("{:<15} |  {:<25} |  {:<25}".format("Field", "Property 1", "Property 2"))
        print("-" * 72)
        for key in ['ID', 'Location', 'Type', 'Price', 'Status']:
            print("{:<15} |  {:<25} |  {:<25}".format(key, prop1[key], prop2[key]))
        print("-" * 72)

    except ValueError:
        print("⚠️  Invalid input! Please enter valid property IDs.")



def suggestProp():
    budget=int(input("\nEnter your max budget: "))
    budgetProp=[]
    for prop in properties:
        if int(prop['Price'].replace(",", "")) <= budget:
            budgetProp.append(prop)
    if budgetProp:
        print(f"\nProperties under Rs.{budget}:\n")
        print("{:<10} {:<15} {:<15} {:<15} {:<15}".format("ID", "Location", "Type", "Price(in Rs)", "Status"))
        print("------------------------------------------------------------------------------------------------")
        for property in budgetProp:
            if property['Status'].lower().strip().startswith('booked by '):
                property['Status']=' Booked'
            print("{:<10} {:<15} {:<15} {:<15} {:<15}".format(property['ID'], property['Location'], property['Type'], property['Price'], property['Status']))
        print("------------------------------------------------------------------------------------------------")
    else:
        print(f"⚠️ : No such properties under budget of Rs.{budget} Found\n")



def bookProp():
    bookInput = input("\nEnter property ID to book: ").strip()
    found = False
    for prop in properties:
        if bookInput == str(prop['ID'].strip()):
            found = True
            if prop['Status'].strip() == 'Available':
                password = getpass("Enter your password to confirm booking: ").strip()
                matched_client = next((c for c in clients if password == c['Password'].strip()), None)
                if not matched_client:
                    print("❌ Client not found. Booking cancelled.")
                    return
                booking_date = datetime.now().strftime("%Y-%m-%d")
                new_status = f"Booked by {matched_client['ID']} on {booking_date}"
                prop['Status'] = new_status
                print(f"✅ Booking successful for property ID {bookInput}.")
                print(f"Status updated to 'Booked'.")
                # Update data/ALLproperties.txt
                with open('data/ALLproperties.txt', 'w') as f:
                    for p in properties:
                        line = f"{p['ID'].strip()} ; {p['Location'].strip()} ; {p['Type'].strip()} ; {p['Price'].strip()} ; {p['Status'].strip()}\n"
                        f.write(line)
                return
            else:
                print(f"⚠️ Property with ID {bookInput} is already booked.")
                return
    if not found:
        print(f"⚠️ No such property with ID {bookInput} found.")



def cancelProp(currentClient):
    cancelInput = input("\nEnter property ID to cancel the booking: ").strip()
    for prop in properties:
        if cancelInput == str(prop['ID']).strip():
            if not prop['Status'].strip().startswith('Booked'):
                print(f"Property with ID {cancelInput} is not yet booked.")
                return
            # Check if currentClient made this booking
            if f"Booked by {str(currentClient['ID'])}" in prop['Status']:
                confirm = input("Are you sure you want to cancel the booking? (y/n): ")
                if confirm.lower() == 'y':
                    prop['Status'] = 'Available'
                    print(f"✅ Booking cancelled for property ID {cancelInput}. Status updated to 'Available'.")
                    # Update data/ALLproperties.txt
                    with open('data/ALLproperties.txt', 'w') as f:
                        for p in properties:
                            line = f"{p['ID'].strip()} ; {p['Location'].strip()} ; {p['Type'].strip()} ; {p['Price'].strip()} ; {p['Status'].strip()}\n"
                            f.write(line)
                    return
                else:
                    print("Cancellation aborted.")
                return
            else:
                print("❌ You are not authorized to cancel this booking. It was booked by another client.")
                return
    print(f"⚠️ No such property with ID {cancelInput} found.")


def adminBookProp():
    if not clients:
        print("⚠️ No clients available.")
        return
    if not properties:
        print("⚠️ No properties available.")
        return
    try:
        client_id = input("Enter client ID to book for: ").strip()
        client = next((c for c in clients if c['ID'].strip() == client_id), None)
        if not client:
            print(f"⚠️ No client found with ID {client_id}.")
            return
        book_input = input("Enter property ID to book: ").strip()
        for prop in properties:
            if book_input == prop['ID'].strip():
                if prop['Status'].strip() == 'Available':
                    prop['Status'] = f'Booked By {client_id} on {datetime.now().strftime("%Y-%m-%d")}'
                    # prop['Booked By'] = client_id
                    print(f"✅ Property ID {book_input} successfully booked for client '{client['Name'].strip()}'.")
                    with open('data/ALLproperties.txt', 'w') as f:
                        for p in properties:
                            line = f"{p['ID'].strip()} ; {p['Location'].strip()} ; {p['Type'].strip()} ; {p['Price'].strip()} ; {p['Status'].strip()}\n"
                            f.write(line)
                        return
                    return
                else:
                    print(f"❌ Property ID {book_input} is already booked.")
                    return
        print(f"⚠️ No property found with ID {book_input}.")
    except ValueError:
        print("❌ Invalid input. Please enter numeric IDs.")


def adminCancelProp():
    global clientBookings
    cancelInput = input("\nEnter property ID to cancel the booking: ")
    for prop in properties:
        if cancelInput == prop['ID']:
            if prop['Status'] != 'Booked':
                print(f"Property with ID {cancelInput} is not yet booked.")
                return
            confirm = input("Are you sure you want to cancel this booking? (y/n): ")
            if confirm.lower() == 'y':
                prop['Status'] = 'Available'
                clientBookings = [b for b in clientBookings if b['property']['ID'] != cancelInput]
                print(f"✅ Booking cancelled for property ID {cancelInput}. Status updated to 'Available'.")
                with open('data/ALLproperties.txt', 'w') as f:
                    for p in properties:
                        line = f"{p['ID'].strip()} ; {p['Location'].strip()} ; {p['Type'].strip()} ; {p['Price'].strip()} ; {p['Status'].strip()}\n"
                        f.write(line)
                return
            else:
                print("Cancellation aborted.")
            return
    print(f"⚠️ No such property with ID {cancelInput} found.")


def addProp():
    global properties
    while True:
        writePropDataToFile()
        properties = readPropFileStoreList()
        print(f"✅ Property record for ID {properties[-1]['ID']} added successfully.\n")
        more = input("Do you want to add more record? (y/n): ").lower()
        if more == 'n':
            break
        elif more != 'y':
            print("⚠️  : Invalid input! Please enter 'y' or 'n'.")


def delProp():
    while True:
        delID = input("\nEnter property ID you want to delete: ").strip()
        found = False
        for prop in properties:
            if delID == prop['ID'].strip():
                confirm = input(f"Are you sure you want to delete the record for property {delID}? (y/n): ").lower()
                if confirm == 'y':
                    properties.remove(prop)
                    # update file
                    with open('data/ALLproperties.txt', 'w') as f:
                        for p in properties:
                            f.write(f"{p['ID'].strip()} ; {p['Location'].strip()} ; {p['Type'].strip()} ; {p['Price'].strip()} ; {p['Status'].strip()}\n")
                    print(f"✅ Record for property ID {delID} deleted successfully.")
                else:
                    print("❌ Deletion cancelled.")
                found = True
                break 
        if not found:
            print(f"⚠️  No such property with ID {delID} found.\n")
        more = input("Do you want to delete more records? (y/n): ").lower()
        if more == 'n':
            break
        elif more != 'y':
            print("⚠️  Invalid input! Please enter 'y' or 'n'.\n")



def viewClients():
    print("\nAll Clients: \n")
    print("-----------------------------------------------------------------------------------------------------------------------")
    print("{:<10} {:<15} {:<20} {:<25} {:<25} {:<15}".format("🆔", "Name🧑", "City🏙️", "Phone Number📞", "Email📧", "Password🔑"))
    print("-----------------------------------------------------------------------------------------------------------------------")
    for c in clients:
        print("{:<10} {:<15} {:<20} {:<25} {:<25} {:<15}".format(c['ID'], c['Name'], c['City'], c['Phone Number'], c['Email'], c['Password']))
    print("-----------------------------------------------------------------------------------------------------------------------")


def viewClientBookings():
    bookings_found = False
    print("\nClient Booking Record:\n")
    print(f"{'Client ID':<12} {'Client Name':<20} {'Property ID':<15} {'Booking Date':<15}")
    print("-" * 70)
    for prop in properties:
        status = prop.get('Status', '').strip()
        if status.lower().startswith("booked by "):
            bookings_found = True
            try:
                parts = status.replace("Booked by ", "").split(" on ")
                client_id = parts[0].strip()
                booking_date = parts[1].strip()
            except (IndexError, ValueError):
                return
                # client_id = "Unknown"
                # booking_date = "Unknown"
            client = next((c for c in clients if str(c['ID']).strip() == client_id.strip()), None)
            client_name = client['Name'] if client else "Unknown"
            print(f"{client_id:<12} {client_name:<20} {prop['ID']:<12} {booking_date:<15}")
    if not bookings_found:
        print("⚠️ : No client bookings found.\n")



def addClient():
    global clients
    writeClientsData()
    clients=readClientFileStoreList()


def removeClient():
    if not clients:
        print("⚠️ No clients available to remove.")
        return
    print("\nREMOVE CLIENT:\n")
    try:
        cID = input("Enter client ID to remove: ").strip()
        client_to_remove = next((c for c in clients if c['ID'].strip() == cID), None)
        if client_to_remove:
            confirm = input(f"Are you sure you want to remove client '{client_to_remove['Name']}'? (y/n): ").lower()
            if confirm == 'y':
                clients.remove(client_to_remove)
                with open('data/ALLclients.txt', 'w') as f:
                    for client in clients:
                        line = f"{client['ID']} ; {client['Name']} ; {client['City']} ; {client['Phone Number']} ; {client['Email']} ; {client['Password']}\n"
                        f.write(line)
                print(f"✅ Client ID {cID} removed successfully.")
            else:
                print("❌ Removal cancelled.")
        else:
            print(f"⚠️ No client found with ID {cID}.")
    except ValueError:
        print("❌ Invalid input. Please enter a numeric Client ID.")



def adminLogin():
    print("\nADMIN LOGIN PORTAL:\n")
    # name=input("Enter your name: ")
    # loginPass=int(input("Enter password: "))
    loginPass = getpass("Enter admin password: ")
    if loginPass==ADMINpassword:
        print("✅ Login successful.\n")
    else:
        print("⚠️ : Incorrect password! \nAdmin access denied❌\n.")
        return -1
    

def registerClient():
    global clients
    register=writeClientsData()
    if register== -1:
        print("⚠️ : Client is already registered. Please login.\n")
        wantLogin = input("Do you want to login? (y/n): ")
        if wantLogin.lower() == 'y':
            loginClient() 
        return
    else:
        clients=readClientFileStoreList()
    

def loginClient():
    print("\nCLIENT LOGIN PORTAL:\n")
    while True:
        choice = int(input("How do you want to login?\n1. With phone number\n2. With email\nEnter choice: "))
        if choice not in [1, 2]:
            print("⚠️ Invalid choice! Please enter 1 or 2.\n")
        else:
            break
    matched_client=None
    if choice == 1:
        while True:
            phone = input("Enter your phone number: ").strip()
            if is_valid_phone(phone):
                break
            else:
                print("❌ Invalid phone number. Must be 10 digits. Please try again.")
        matched_client = next((c for c in clients if phone == c['Phone Number'].strip()), None)
        if not matched_client:
            print("⚠️ Phone number is not registered.")
            wantRegister = input("Do you want to register? (y/n): ")
            if wantRegister.lower() == 'y':
                registerClient()
            return -1
        while True:
            loginPass = getpass("Enter password: ").strip()
            if loginPass == matched_client['Password'].strip():
                print("✅ Login successful.\n")
                return matched_client
            else:
                print("⚠️ : Incorrect credentials! Client access denied.❌ \nPlease try again.")
    elif choice == 2:
        while True:
            email = input("Enter your email: ").strip()
            if is_valid_email(email):
                break
            else:
                print("⚠️ : Incorrect credentials! Client access denied.❌ \nPlease try again.")
        matched_client = next((c for c in clients if email.lower() == c['Email'].lower().strip()), None)
        if not matched_client:
            print("⚠️ Email is not registered.")
            wantRegister = input("Do you want to register? (y/n): ")
            if wantRegister.lower() == 'y':
                registerClient()
            return -1
        while True:
            loginPass = getpass("Enter password: ").strip()
            if loginPass == matched_client['Password'].strip():
                print("✅ Login successful.\n")
                return matched_client
            else:
                print("⚠️ : Incorrect credentials! Client access denied.❌ \nPlease try again.\n")





def changePass():
    global clients
    email = input("Enter your email: ").strip()
    if not is_valid_email(email):
        print("❌ Invalid email format.")
        return
    password = getpass("Enter your current password: ").strip()
    matched_client = None
    for c in clients:
        if c['Email'].strip() == email and c['Password'].strip() == password:
            matched_client = c
            break
    if not matched_client:
        print("❌ No matching client found with that email and password.")
        return
    while True:
        new_password = getpass("Enter new password: ").strip()
        confirm_password = getpass("Confirm new password: ").strip()

        if new_password != confirm_password:
            print("❌ Passwords do not match. Try again.")
        elif new_password == password:
            print("❌ New password cannot be the same as the old password.")
        else:
            break
    matched_client['Password'] = new_password
    with open("data/ALLclients.txt", "w") as f:
        for client in clients:
            line = f"{client['ID']} ; {client['Name']} ; {client['City']} ; {client['Phone Number']} ; {client['Email']} ; {client['Password']}\n"
            f.write(line)
    print("✅ Password changed successfully.")


def AdminChangePass():
    global ADMINpassword
    password = getpass("Enter current password: ").strip()
    if password != ADMINpassword.strip():
        print("❌ Incorrect current password.")
        return
    while True:
        new_password = getpass("Enter new password: ").strip()
        confirm_password = getpass("Confirm new password: ").strip()
        if new_password != confirm_password:
            print("❌ Passwords do not match. Try again.")
        elif new_password == password:
            print("❌ New password cannot be the same as the old password.")
        else:
            break
    ADMINpassword = new_password
    print("✅ Admin password changed successfully.")




def adminMain():
    loginStatus=adminLogin()
    if loginStatus!=-1:
        while True:
            try:
                adminMenu()
                choice=int(input("\nEnter your choice: "))
                if choice==1:
                    viewProp()
                elif choice==2:
                    searchByLoc()
                elif choice==3:
                    searchByType()
                elif choice==4:
                    searchByPrice()
                elif choice==5:
                    viewPropDetails()
                elif choice==6:
                    adminBookProp()
                elif choice==7:
                    adminCancelProp()
                elif choice==8:
                    compareProp()
                elif choice==9:
                    suggestProp()
                elif choice==10:
                    sortPropByPrice()
                elif choice==11:
                    addProp()
                elif choice==12:
                    delProp()
                elif choice==13:
                    viewClients()
                elif choice==14:
                    viewClientBookings()
                elif choice==15:
                    addClient()
                elif choice==16:
                    removeClient()
                elif choice==17:
                    AdminChangePass()
                elif choice==18:
                    print("\nExitting Admin Portal.\nGoodbye!...🤗\n")
                    break
                else:
                    print("⚠️  : Invalid choice!\n")
            except ValueError:
                print("⚠️  : Invalid input! Enter only numeric value.\n")


def clientMain():
    currentClient = loginClient()
    if currentClient != -1:
        while True:
            try:
                clientMenu()
                choice=int(input("\nEnter your choice: "))
                if choice==1:
                    viewProp()
                elif choice==2:
                    searchByLoc()
                elif choice==3:
                    searchByType()
                elif choice==4:
                    searchByPrice()
                elif choice==5:
                    viewPropDetails()
                elif choice==6:
                    bookProp()
                elif choice==7:
                    cancelProp(currentClient)
                elif choice==8:
                    compareProp()
                elif choice==9:
                    suggestProp()
                elif choice==10:
                    sortPropByPrice()
                elif choice==11:
                    changePass()
                elif choice==12:
                    print("\nExitting Client Portal.\nGoodbye!...🤗\n")
                    break
                else:
                    print("⚠️  : Invalid choice!\n")
            except ValueError:
                print("⚠️  : Invalid input! Enter only numeric value.\n")


def guestMain():
    while True:
        try:
            guestMenu()
            choice=int(input("\nEnter your choice: "))
            if choice==1:
                viewProp()
            elif choice==2:
                searchByLoc()
            elif choice==3:
                searchByType()
            elif choice==4:
                searchByPrice()
            elif choice==5:
                viewPropDetails()
            elif choice==6:
                compareProp()
            elif choice==7:
                suggestProp()
            elif choice==8:
                sortPropByPrice()
            elif choice==9:
                print("\nExitting Guest Portal.\nGoodbye!...🤗\n")
                break
            else:
                print("⚠️  : Invalid choice!\n")
        except ValueError:
            print("⚠️  : Invalid input! Enter only numeric value.\n")



def main():
    readPropFileStoreList()
    readClientFileStoreList()
    # print(properties)
    # print(clients)
    # print(clientBookings)
    welcomeScreen()
    while True:
        try:
            print("---------------------------------------------------------")
            print("\nHow do you want to visit this portal?\n")
            print("1️⃣  Register client\n2️⃣  Login as Client\n3️⃣  Login as admin\n4️⃣  Guest user\n5️⃣  Exit")
            print("---------------------------------------------------------")
            choice=int(input("\nEnter your choice: "))
            if choice==1:
                registerClient()
            elif choice==2:
                clientMain()
            elif choice==3:
                adminMain()
            elif choice==4:
                guestMain()
            elif choice==5:
                print("\n😊 Thank you for using Python Real Estate Portal.😊\nGoodbye!...🤗\n")
                break
            else:
                print("⚠️  : Invalid choice!\n")
        except ValueError:
            print("⚠️  : Invalid input! Enter only numeric value.\n")






main()
