from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv
import os


def get_list(el):
    return [e.text for e in el]

def format_csv(data):
    lines = (','.join(pair) for pair in data)
    return '\n'.join(lines) + '\n'

# path to folder with out trailing slash would be next
def save_csv(folder, trend_name, data):
    folder += '/'
    path_top = folder + 'top/'
    path_ris = folder + 'rising/'
    file_name_top = path_top + trend_name + "_top.csv"
    file_name_rising = path_ris + trend_name + '_rising.csv'

    # making some folders STOCK --> TOP, RISING
    if not os.path.exists(folder):
        os.makedirs(folder)
        if not os.path.exists(path_top):
            os.makedirs(path_top)
        if not os.path.exists(path_ris):
            os.makedirs(path_ris)
    try:
        top_csv = format_csv(data['top'])

        with open(file_name_top, mode='w') as f:
            f.write(top_csv)
    except KeyError:
        print('No Top Data for %s' % (trend_name))
    # might not have rising data
    try:
        rising_csv = format_csv(data['rising'])
        with open(file_name_rising, mode='w') as f:
            f.write(rising_csv)

    except KeyError:
        print('No Rising Data for %s' % (trend_name))

def get_stuff(url):
    driver.get(url)
    time.sleep(3)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    data = {}
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "fe-atoms-generic-content-container")))
    except TimeoutException:
        print "Loading took too much time!"
        return {'top': ('', '')}

    time.sleep(3)
    # 0th element will be related topics
    related_queries = driver.find_elements_by_class_name('fe-related-queries')[1]
    texts_rising = related_queries.find_elements_by_class_name("label-text")
    try:
        current = related_queries.find_element_by_class_name('_md-text')
    except:
        # happens when there is no TOP or RISING data for a stock ticker
        return {}
    rising_txt = get_list(texts_rising)
    if current.text == 'Top':
        values_top = related_queries.find_elements_by_class_name('progress-value')
        top_val = get_list(values_top)
        zip_rising = zip(rising_txt, top_val)
        data['top'] = zip_rising
        return data
    else:
        values_rising = related_queries.find_elements_by_class_name('rising-value')
        rising_val = get_list(values_rising)
        zip_rising = zip(rising_txt, rising_val)
        data['rising'] = zip_rising

    # data['rising'] = {key: value for key, value in zip(rising_txt, rising_val)}

    nav = related_queries.find_element_by_class_name('bullets-view-selector')
    nav.click()
    # there are 5 dropdown menus on the page, the last one will be for related queries
    menu = driver.find_elements_by_class_name('_md-select-menu-container')[4]
    # click on top
    top = menu.find_elements_by_tag_name('md-option')[1]
    top.click()

    top_queries = driver.find_elements_by_class_name('fe-related-queries')[1]
    texts_top = top_queries.find_elements_by_class_name("label-text")
    values_top = top_queries.find_elements_by_class_name('progress-value')


    top_txt = get_list(texts_top)
    top_val = get_list(values_top)
    zip_top = zip(top_txt, top_val)
    data['top'] = zip_top
    # data['top'] = {key: value for key, value in zip(top_txt, top_val)}
    return data


driver = webdriver.Firefox()
stocks = ['AAPL', 'ABBV', 'ABI', 'ABK', 'ABT']
for stock in stocks:
    for i in xrange(2004, 2014):
        year = i
        go_to = 'https://www.google.com/trends/explore?date={0}-01-01%20{0}-12-31&geo=US&q={1}'.format(year, stock)
        print ("Accessing " + go_to)
        save_csv(stock, '%s_%s' % (stock, i), get_stuff(go_to))
