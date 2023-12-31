# #!/usr/bin/python3

# # Author Nick Chesser
# # About Screen Scraper Class for Instagram

# # Imports
# import os

# # Selenium
# from selenium import webdriver
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException

# # Constants
# FILEPATH = os.path.dirname(os.path.realpath(__file__))
# FIREFOX_DRIVER = f"{FILEPATH}/utilities/geckodriver"

# # # Windows Drivers
# # FIREFOX_DRIVER = f"{FILEPATH}/geckodriver.exe"
# FIREFOX_BINARY = r"C:\Program Files\Mozilla Firefox\firefox.exe"

# # Credentials
# from constants import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, INSTAGRAM_URL


# class InstagramScraper:
#     def __init__(self, username: str, password: str, url: str = INSTAGRAM_URL):
#         # Options
#         self.username = username
#         self.password = password
#         self.url = url
        
#         # Using Chrome for Now
#         self.driver = webdriver.Chrome() 

#         # # Setup Firefox Options
#         # self.firefox_options = FirefoxOptions()
#         # self.firefox_options.binary_location = FIREFOX_BINARY # For Windows
#         # # self.firefox_options.add_argument('--headless')
#         # # self.firefox_service = Service(FIREFOX_DRIVER)

#         # # Setup Driver
#         # # self.driver = webdriver.Firefox(service=self.firefox_service, options=self.firefox_options)
#         # self.driver = webdriver.Firefox(options=self.firefox_options)
        
#         # Wait for Components
#         self.wait = WebDriverWait(self.driver, 15)


#     def __str__(self):
#         print(', '.join(self.active_alerts))


#     # Getters
#     def return_active_alerts(self):
#         return self.active_alerts
    
    
#     def click_button(self, button_text: str):
#         try:
#             # Wait for the button to be clickable
#             button = WebDriverWait(self.driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, f'//svg[@aria-label="{button_text}"]'))
#             )

#             # Click the button
#             button.click()
#         except Exception as e:
#             print(f"Error clicking the '{button_text}' button: {e}")


#     # Functions
#     def wait_for_element(self, element):
#         attempts = 0
#         while attempts < 3:
#             try:
#                 element = self.wait.until(EC.presence_of_element_located(element))
#                 print('Element Found!', element.text)
#                 return element
#             except TimeoutException:
#                 attempts += 1
#                 print('Could Not Find Element', element)

#         return False


#     def login(self):
#         '''Login to Instagram'''
#         try:
#             # Load URL
#             self.driver.get(self.url)

#             # Wait for login page to load
#             self.wait_for_element((By.NAME, 'username'))

#             # Fill out form
#             username_element = self.driver.find_element(By.NAME, 'username')
#             username_element.clear()
#             username_element.send_keys(self.username)

#             password_element = self.driver.find_element(By.NAME, 'password')
#             password_element.clear()
#             password_element.send_keys(self.password)

#             # Run Submit
#             password_element.submit()
            
#             print('Logged In!')
            
#         except Exception as e:
#             print(f'Error during login: {e}')


#     def upload_photo(self):
#         '''Get Active ExtraHop Alerts'''
#         # Login to Portal
#         self.login()
#         print('Loaded Page After Login...')

#         # # Wait for Alerts Page to Load
#         # self.wait_for_element((By.CLASS_NAME, '_a3wf system-fonts--body segoe'))
#         # print('Loaded Page After Login...')
#         self.wait_for_element((By.CLASS_NAME, 'New post'))
        
#         # Click Create Button
#         self.click_button('New post')
#         print('Clicked New Post')
        
#         self.wait_for_element((By.CLASS_NAME, 'New post'))
        
        
#         # Close the instance
#         self.driver.quit()


# def main():
#     print("Running Screen Scrape...")
#     ss = InstagramScraper(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
#     ss.upload_photo()


# if __name__ == "__main__":
#     main()