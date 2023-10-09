from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from pandas.testing import assert_frame_equal
import time
import winsound




def refresh_stubhub_site():
    global driver
    driver.refresh()
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # # Extract the ticket prices
    # prices = []
    # for item in soup.find_all(class_='sc-elSRXu fgjIaR'):
    #     prices.append(item.text)

    # # Create a Pandas dataframe to store the ticket prices
    # df = pd.DataFrame({'Ticket Prices': prices})

    # # Print the dataframe
    # return(df)
    # find all the ticket listings
    listings = soup.find_all('div', {'class': 'sc-bpSicm'})
    
    # create a list to store the extracted data
    ticket_data = []
    
    # loop through each ticket listing and extract the relevant information
    for listing in listings:
        name = listing.find('div', {'class': 'sc-elSRXu'}).text
        price = listing.find('div', {'class': 'sc-elSRXu fgjIaR'}).text
        available = True if listing.find('button', {'class': 'sc-fujyAs'}) is None else False
        sold_text = listing.find('button', {'class': 'sc-fujyAs'}).text if not available else ''
        
        ticket_data.append({'Name': name, 'Price': price, 'Available': available, 'Sold': sold_text})
    
    # create a pandas DataFrame from the extracted data and return it
    df_ticket_data = pd.DataFrame(ticket_data)
    # df_ticket_data = df_ticket_data[df_ticket_data['Sold'].str.contains('Select')] #drop the sold ones
    return pd.DataFrame(ticket_data)


starter_url = 'https://www.stubhub.com/electric-daisy-carnival-las-vegas-edc-las-vegas-tickets-5-19-2023/event/150214580/?quantity=1'
previous_output = ""
firefox_binary = FirefoxBinary()
driver = webdriver.Firefox(firefox_binary=firefox_binary)
driver.get(starter_url)

#every Five seconds check if a new ticket has been listed on the site. If so beep alternating tones to alert the user. 
while True:
    current_output = refresh_stubhub_site()
    if isinstance(previous_output, pd.DataFrame): 
        diff = assert_frame_equal(current_output, previous_output, check_exact=True)
        if diff != None:
            print(f"Ticket Price Changed:\n {diff}")        
            for i in range(7):
                winsound.Beep(440  , 500  )
                winsound.Beep(640, 500)
                # Future State: Send notification to user here, e.g. using email, SMS, or a messaging service

    previous_output = current_output
    time.sleep(5)