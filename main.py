import sys
import os
import json
import requests
import secrets
import time
from password_strength import PasswordPolicy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_settings():
    with open('settings.json') as f:
        return json.load(f)

def generate_random_username():
    return ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(10))

def generate_strong_password():
    policy = PasswordPolicy.from_names(
        length=12,
        uppercase=1,
        numbers=1,
        special=1,
    )
    return secrets.token_urlsafe(20)

def write_to_file(username, password):
    # Your directory
    directory = r'C:\Users\licen\Downloads\roblox-account-generator-main\roblox-account-generator-main'
    
    # Construct the full path to the accounts.txt file
    file_path = os.path.join(directory, 'accounts.txt')
    
    # Write username and password to the accounts.txt file
    with open(file_path, 'a') as file:
        file.write(f"{username}:{password}\n")

    # Print username and password to command line
    print(f"{username}:{password}")

def create_roblox_account(username, password, email):
    url = "https://www.roblox.com/CreateAccount"
    data = {
        "username": username,
        "password": password,
        "confirmPassword": password,
        "birthday": "2000-01-01",
        "gender": "Male",
        "email": email,
        "parentEmail": "",
        "passwordStrength": "Good",
        "context": "HomeSignup",
        "referrer": "",
        "flock": "",
        "refPage": "",
        "tbsa": "",
        "nTickets": ""
    }
    response = requests.post(url, data=data)  # Make the POST request
    print("Response:", response.text)  # Print the response text

    # Check if the account was created successfully
    if "Your account has been created!" in response.text:
        print(f"Roblox account created: {username}")
        write_to_file(username, password)  # Write to file if account creation is successful
    else:
        print(f"Failed to create Roblox account: {username}")

def solve_captcha():
    # Your code for solving CAPTCHA using Anti-Captcha service goes here
    pass

def browser_automation_create_roblox_account(username, password, headless=True):
    # Set Chrome options
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument('--headless')  # Run in headless mode if headless=True
    chrome_options.add_argument('--incognito')

    # Initialize the browser driver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)
    
    # Open the Roblox signup page
    driver.get("https://www.roblox.com/CreateAccount")

    # Fill out the month
    month_select = Select(driver.find_element(By.ID, "MonthDropdown"))
    month_select.select_by_value("Jan")

    # Fill out the day
    day_select = Select(driver.find_element(By.ID, "DayDropdown"))
    day_select.select_by_value("01")

    # Fill out the year
    year_select = Select(driver.find_element(By.ID, "YearDropdown"))
    year_select.select_by_value("2000")

    # Fill out the username
    username_input = driver.find_element(By.ID, "signup-username")
    username_input.send_keys(username)

    # Fill out the password
    password_input = driver.find_element(By.ID, "signup-password")
    password_input.send_keys(password)

    # Find and click on the male icon
    male_icon = driver.find_element(By.CLASS_NAME, "gender-male")
    male_icon.click()

    # Wait for the signup button to become clickable
    signup_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "signup-button"))
    )
    
    # Submit the form
    signup_button.click()
    
    # Wait for the signup process to complete
    time.sleep(0.005)

    # Write to file if account creation is successful
    write_to_file(username, password)

    # Close the browser
    driver.quit()

def main():
    # Load settings from settings.json
    settings = load_settings()

    # Extract settings
    capsolver_key = settings['capsolver_key']
    thread_count = settings['thread_count']
    verify_mail = settings.get('verify_mail', False)

    paused = False

    while True:
        # Ask user to choose action
        if not paused:
            print("Choose action:")
            print("1. Continue")
            print("2. Pause")
            print("3. Stop")
            action = input("Enter your action (1, 2, or 3): ")
        else:
            print("Paused. Choose action:")
            print("1. Continue")
            print("3. Stop")
            action = input("Enter your action (1 or 3): ")

        # Execute action
        if action == '1':
            # Continue execution
            if not paused:
                print("Continuing...")
            paused = False
        elif action == '2':
            # Pause execution
            paused = True
        elif action == '3':
            # Stop execution
            print("Execution stopped.")
            break
        else:
            print("Invalid action. Please enter '1', '2', or '3'.")

        # If paused, wait for user to continue
        if paused:
            input("Press Enter to continue...")

        # Create Roblox accounts based on user's choice
        if not paused:
            # Ask user to choose method
            print("Choose account creation method:")
            print("1. Roblox API method")
            print("2. Browser automation method")
            choice = input("Enter your choice (1 or 2): ")

            # Create Roblox accounts based on user's choice
            if choice == '1':
                # Roblox API method
                for i in range(thread_count):
                    username = generate_random_username()
                    password = generate_strong_password()
                    email = f"user{i+1}@example.com"  
                    create_roblox_account(username, password, email)
                    time.sleep(0.005)
            elif choice == '2':
                # Browser automation method
                for i in range(thread_count):
                    username = generate_random_username()
                    password = generate_strong_password()
                    browser_automation_create_roblox_account(username, password)
                    time.sleep(0.005)
            else:
                print("Invalid choice. Please enter '1' or '2'.")

if __name__ == "__main__":
    main()
