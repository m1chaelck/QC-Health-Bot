import time
import random
import tkinter as tk
import os.path
from config import *
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

# details for the login form.
payload = {
    'firstname': config_payload['firstname'],
    'lastname': config_payload['lastname'],
    'insurance_num': config_payload['insurance_num'],
    'insurance_seq_num': config_payload['insurance_seq_num'],
    'dob_day': config_payload['dob_day'],
    'dob_month': config_payload['dob_month'],
    'dob_year': config_payload['dob_year'],
    'sex': config_payload['sex'],
    'range_perimeter': config_payload['range_perimeter'],
    'reason': config_payload['reason']
}

def huminized_input(element, s: str) -> None:
    for char in s:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.7))
def logged_in_check():
    try:
        DRIVER.find_element_by_class_name('ctl00$ContentPlaceHolderMP$AssureForm_FirstName')
        return False
    except:
        return True
    
def get_user_payload():
    '''
    Generate user payload from the console user input.
    '''
    # ask for user input
    first_name = input('Enter your first name: ')
    last_name = input('Enter your last name: ')
    insurance_num = input('Enter your insurance number: ')
    insurance_seq_num = input('Enter your insurance sequence number: ')
    dob_day = input('Enter your date of birth day: ')
    dob_month = input('Enter your date of birth month: ')
    dob_year = input('Enter your date of birth year: ')
    sex = input("Enter 'M' or 'F'")
    range_perimeter = input("Enter '25km', '50km' or '100km'")
    reason = input("Enter 'minor emergency' or 'priority consultation'")
    # generate user payload
    payload.get('firstname').append(first_name)
    payload.get('lastname').append(last_name)
    payload.get('insurance_num').append(insurance_num)
    payload.get('insurance_seq_num').append(insurance_seq_num)
    payload.get('dob_day').append(dob_day)
    payload.get('dob_month').append(dob_month)
    payload.get('dob_year').append(dob_year)
    payload.get('sex').append(sex)
    payload.get('range_perimeter').append(range_perimeter)
    payload.get('reason').append(reason)
    print('User payload generated successfully!')

def print_clinics():
    clinics = DRIVER.find_elements(By.XPATH, '//div[@class="tmbClinic"]')
    for clinic in clinics:
        print(clinic.text)

if __name__ == "__main__":
    
    # # Create the tkinter window
    # window = tk.Tk()
    # window.title("RVSQ Booking Login Form")

    # # Create labels for each field
    # tk.Label(window, text="First Name:").grid(row=0, column=0)
    # tk.Label(window, text="Last Name:").grid(row=1, column=0)
    # tk.Label(window, text="Insurance Number:").grid(row=2, column=0)
    # tk.Label(window, text="Insurance Sequence Number:").grid(row=3, column=0)
    # tk.Label(window, text="DOB Day:").grid(row=4, column=0)

    # tk.Label(window, text="Sex (M/F):").grid(row=5, column=0)
    # tk.Label(window, text="Range Perimeter:").grid(row=6, column=0)
    # tk.Label(window, text="Reason:").grid(row=7, column=0)

    # # Create entry fields for each input
    # firstname_entry = tk.Entry(window)
    # lastname_entry = tk.Entry(window)
    # insurance_num_entry = tk.Entry(window)
    # insurance_seq_num_entry = tk.Entry(window)
    # dob_day_entry = tk.Entry(window, width=2)
    # dob_month_entry = tk.Entry(window, width=2)
    # dob_year_entry = tk.Entry(window, width=4)
    # sex_entry = tk.Entry(window)
    # range_perimeter_entry = tk.Entry(window)
    # reason_entry = tk.Entry(window)

    # # Add entry fields to the window grid
    # firstname_entry.grid(row=0, column=1)
    # lastname_entry.grid(row=1, column=1)
    # insurance_num_entry.grid(row=2, column=1)
    # insurance_seq_num_entry.grid(row=3, column=1)
    # dob_day_entry.grid(row=4, column=1)
    # dob_month_entry.grid(row=4, column=3)
    # dob_year_entry.grid(row=4, column=5)
    # sex_entry.grid(row=5, column=1)
    # range_perimeter_entry.grid(row=6, column=1)
    # reason_entry.grid(row=7, column=1)

    # # Create radio buttons for range perimeter
    # range_perimeter_var = tk.StringVar()
    # range_perimeter_var.set('0')
    # range_perimeter_frame = tk.Frame(window)
    # range_perimeter_frame.grid(row=6, column=1)

    # for i, (text, value) in enumerate([('25km', '0'), ('50km', '1'), ('100km', '2')]):
    #     tk.Radiobutton(range_perimeter_frame, text=text, variable=range_perimeter_var, value=value).grid(row=0, column=i)

    # # Create a button to submit the form
    # submit_button = tk.Button(window, text="Submit")
    # submit_button.grid(row=8, column=1)

    # # Run the tkinter event loop
    # window.mainloop()
    
    # time.sleep(500)

    #webdriver setup
    URL = 'https://rvsq.gouv.qc.ca/prendrerendezvous/Default.aspx?culture=en'
    CHROME_DRIVER_PATH = './chromedriver.exe'
    SERVICE = Service(CHROME_DRIVER_PATH)
    options = webdriver.ChromeOptions()
    # options.headless = True
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("detach", True)
    DRIVER = webdriver.Chrome(service=SERVICE, options=options)
    DRIVER.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    
    config_file = os.path.isfile('./config.py')
    response = DRIVER.get(URL)
    wait = WebDriverWait(DRIVER, 20)
    time.sleep(random.uniform(1, 3))
    LOGGED_IN = False

    first_name_field = wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolderMP$AssureForm_FirstName')))
    huminized_input(first_name_field, payload["firstname"])
    time.sleep(random.uniform(1, 3))

    last_name_field = wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolderMP$AssureForm_LastName')))
    huminized_input(last_name_field, payload["lastname"])
    time.sleep(random.uniform(1, 3))

    insurance_num_field = wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolderMP$AssureForm_NAM')))
    huminized_input(insurance_num_field, payload["insurance_num"])
    time.sleep(random.uniform(1, 3))

    insurance_seq_num_field = wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolderMP$AssureForm_CardSeqNumber')))
    huminized_input(insurance_seq_num_field, payload["insurance_seq_num"])
    time.sleep(random.uniform(1, 3))

    dob_day_field = wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolderMP$AssureForm_Day')))
    huminized_input(dob_day_field, payload["dob_day"])
    time.sleep(random.uniform(1, 3))

    dob_month_field = Select(wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolderMP$AssureForm_Month'))))
    dob_month_field.select_by_value(payload["dob_month"])
    time.sleep(random.uniform(1, 3))

    dob_year_field = wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolderMP$AssureForm_Year')))
    huminized_input(dob_year_field, payload["dob_year"])
    time.sleep(random.uniform(1, 3))

    radio_button = wait.until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolderMP_MaleGender')))
    radio_button.click()

    confirm_btn = wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolderMP$myButton')))
    confirm_btn.click()
    time.sleep(random.uniform(2, 5))
    
    payload_failed = DRIVER.find_elements(By.XPATH, '//label[@class="control-label" and text()="The characters you have entered do not match."]')
    while payload_failed:
        time.sleep(random.uniform(2, 5))
        confirm_btn = wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolderMP$myButton')))
        confirm_btn.click()
        time.sleep(random.uniform(2, 5))
        try:
            payload_failed = DRIVER.find_elements(By.XPATH, '//label[@class="control-label" and text()="The characters you have entered do not match."]')
        except:
            break

    LOGGED_IN = True
    print("Logged in successfully")
    
    link = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="aspnetForm"]/div[3]/div/div/div[1]/div[6]/div/div[1]/div[7]/div/ul/li[1]/a/div')))
    link.click()
    time.sleep(random.uniform(2, 5))
    
    range_perimeter_select = Select(wait.until(EC.presence_of_element_located((By.NAME, 'perimeterCombo'))))
    range_perimeter_select.select_by_value(payload["range_perimeter"]["100km"])
    time.sleep(random.uniform(1, 3))
    
    reason_select = Select(wait.until(EC.presence_of_element_located((By.ID, 'consultingReason'))))
    reason_select.select_by_value(payload['reason']['priority consultation'])
    time.sleep(random.uniform(1, 3))
    
    search_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'h-SearchButton')))
    search_btn.click()
    time.sleep(random.uniform(5, 8))
    #scroll down to the bottom of the page
    DRIVER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    start_time = time.time()
    
    while True:
        try:
            result_clinics = wait.until((EC.presence_of_element_located((By.CLASS_NAME, 'tmbClinic'))))
            if result_clinics:
                tk.messagebox.showinfo(title="Clinic found", message="Clinic found")
                print("\007")
                print_clinics()
                break
        except:
            if not logged_in_check():
                print("Logged out")
                LOGGED_IN = False
                break
            time.sleep(random.uniform(30, 60))
            search_btn.click()
            time.sleep(random.uniform(5, 8))
            #scroll down to the bottom of the page
            DRIVER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # check if the window is still open
    print("---RUNTIME ---")
    print("--- %s hours ---" % ((time.time() - start_time)/3600))
    print("--- %s minutes ---" % ((time.time() - start_time)/60))  
    print("--- %s seconds ---" % (time.time() - start_time))
    DRIVER.quit()
    