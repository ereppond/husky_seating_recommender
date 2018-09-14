import pandas as pd
import numpy as np 
from selenium.webdriver import Chrome

browser = Chrome()
url = 'https://www.tickpick.com/buy-washington-huskies-vs-arizona-state-sun-devils-tickets-husky-stadium---wa-9-22-18-7PM/3330066/'
browser.get(url)

def scrape_listings(browser):
    '''Scrapes ticket listings from tickpick.com
    
    Parameters:
        browser (selenium object): Chrome object on which the scraping will occur
        
    Returns:
        df (DataFrame): cleaned data from website
            -deal rating
            -price
            -available tickets
            -section
            -row
            -tickpick rating
    '''
    df = []
    sel = 'div.listing'
    ticket_info = browser.find_elements_by_css_selector(sel)
    ticket_info = [tic.text.split('\n') for tic in ticket_info]
    for ticket in ticket_info:
        ticket_dict = {}
        ticket_dict['deal_rating'] = ticket[0]
        ticket_dict['price'] = ticket[1].split('$')[1]
        ticket_dict['avail_tics'] = ticket[3]
        ticket_dict['Section'] = ticket[-3].split(' ')[1]
        ticket_dict['Row'] = ticket[-3].split(' ')[-1]
        ticket_dict['rating'] = ticket[-2].split('★')[0]
        df.append(ticket_dict)
    df = pd.DataFrame(df)
    return df


vs_asu = scrape_listings(browser)

# BYU

browser.get('https://www.tickpick.com/buy-washington-huskies-vs-byu-cougars-tickets-husky-stadium---wa-9-29-18-3AM/3330067/')

vs_byu = scrape_listings(browser)

# CU

browser.get('https://www.tickpick.com/buy-washington-huskies-vs-colorado-buffaloes-tickets-husky-stadium---wa-10-20-18-3AM/3330068/')

vs_cu = scrape_listings(browser)

# Stanford

browser.get('https://www.tickpick.com/buy-washington-huskies-vs-stanford-cardinal-tickets-husky-stadium---wa-11-3-18-3AM/3330069/')

vs_stanford = scrape_listings(browser)

# OSU

browser.get('https://www.tickpick.com/buy-washington-huskies-vs-oregon-state-beavers-tickets-husky-stadium---wa-11-17-18-3AM/3330070/')

vs_osu = scrape_listings(browser)

# Converting numerical columns to integers

def conversions(conv, columns):
    for item in columns:
        vs_asu[item] = vs_asu[item].astype(conv)
        vs_byu[item] = vs_byu[item].astype(conv)
        vs_cu[item] = vs_cu[item].astype(conv)
        vs_stanford[item] = vs_stanford[item].astype(conv)
        vs_osu[item] = vs_osu[item].astype(conv)

conversions(int, ['Row','Section','avail_tics', 'price', 'rating'])

vs_asu.dtypes

vs_asu.to_csv('asu.csv')
vs_cu.to_csv('cu.csv')
vs_stanford.to_csv('stanford.csv')
vs_osu.to_csv('osu.csv')
vs_byu.to_csv('byu.csv')

def d_duplicates(df):
    df.drop_duplicates(subset=['Section', 'Row'], inplace=True)
    return df

asu = d_duplicates(vs_asu)
cu = d_duplicates(vs_cu)
byu = d_duplicates(vs_byu)
stanford = d_duplicates(vs_stanford)
osu = d_duplicates(vs_osu)