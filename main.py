import os
import json
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
    directory = r'C:\Users\licen\Downloads\roblox-account-generator-main\roblox-account-generator-main'
    file_path = os.path.join(directory, 'accounts.txt')
    
    with open(file_path, 'a') as file:
        file.write(f"{username}:{password}\n")
    print(f"{username}:{password}")

def browser_automation_create_roblox_account(username, password, headless=True):
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--incognito')

    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get("https://www.roblox.com/CreateAccount")

    month_select = Select(driver.find_element(By.ID, "MonthDropdown"))
    month_select.select_by_value("Jan")

    day_select = Select(driver.find_element(By.ID, "DayDropdown"))
    day_select.select_by_value("01")

    year_select = Select(driver.find_element(By.ID, "YearDropdown"))
    year_select.select_by_value("2000")

    username_input = driver.find_element(By.ID, "signup-username")
    username_input.send_keys(username)

    password_input = driver.find_element(By.ID, "signup-password")
    password_input.send_keys(password)

    male_icon = driver.find_element(By.CLASS_NAME, "gender-male")
    male_icon.click()

    signup_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "signup-button"))
    )
    
    signup_button.click()
    
    time.sleep(0.005)

    write_to_file(username, password)

    driver.quit()

def main():
    settings = load_settings()
    thread_count = settings['thread_count']
    paused = False

    while True:
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

        if action == '1':
            if not paused:
                print("Continuing...")
            paused = False
        elif action == '2':
            paused = True
        elif action == '3':
            print("Execution stopped.")
            break
        else:
            print("Invalid action. Please enter '1', '2', or '3'.")

        if paused:
            input("Press Enter to continue...")

        if not paused:
            for i in range(thread_count):
                username = generate_random_username()
                password = generate_strong_password()
                browser_automation_create_roblox_account(username, password)
                time.sleep(0.005)

if __name__ == "__main__":
    main()
