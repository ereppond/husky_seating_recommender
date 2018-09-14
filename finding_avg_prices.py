import pandas as pd
from selenium.webdriver import Chrome

asu = pd.read_csv('ticket_data/asu.csv').drop('Unnamed: 0', axis=1)
asu = asu[['Section', 'Row', 'price']]

def find_prices(browser):
    '''Scrapes tickpick for prices and cleans the data to put into comprehensive dataframe
    
    Parameters:
        browser (selenium object): Chrome object on which the scraping will occur
        
    Returns:
        prices (list[dictionaries]): pricing data from website (only price, section, and row)
    
    '''
    tickets = browser.find_elements_by_css_selector('li.ticket')
    tickets = [tickets[i].text.split('\n') for i in range(len(tickets))]
    prices = []
    for ticket in tickets:
        sec = ticket[0].split(', ')[0].split(' ')[-1]
        if len(ticket[0].split(', ')) == 1:
            row = 'Zone Seating'
        else:
            row = ticket[0].split(', ')[1].split(' ')[-1]
        price = int(ticket[-1].split('/')[0][1:])
        curr = {'Section': sec, 'Row': row, 'price': price}
        prices.append(curr)
    return prices

# BYU

browser = Chrome()
browser.get('https://www.rateyourseats.com/tickets/events/byu-cougars-at-washington-huskies-september-29-2018-2530479')

byu = find_prices(browser)

# CU

browser = Chrome()
url = 'https://www.rateyourseats.com/tickets/events/colorado-buffaloes-at-washington-huskies-october-20-2018-2530480'

cu = find_prices(browser)

# Stanford

browser = Chrome()
url = 'https://www.rateyourseats.com/tickets/events/stanford-cardinal-at-washington-huskies-november-3-2018-2530481'

stanford = find_prices(browser)

# OSU

browser = Chrome()
url = 'https://www.rateyourseats.com/tickets/events/oregon-state-beavers-at-washington-huskies-november-17-2018-2530482'

osu = find_prices(browser)

# Finalizing data 

# Converting into pandas dataframe

cu = pd.DataFrame(cu)
stanford = pd.DataFrame(stanford)
osu = pd.DataFrame(osu)
byu = pd.DataFrame(byu)

# Find average price based on section and row

avg_price = pd.concat([asu, cu, stanford, osu, byu]).groupby(['Section', 'Row']).mean().reset_index()

# Round to second decimal

avg_price['price'] = avg_price['price'].round(2)

avg_price

