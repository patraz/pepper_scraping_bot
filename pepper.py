from datetime import datetime
from requests_html import HTML
from send_mail import Emailer

import os
import requests
import time

BASE_DIR = os.path.dirname(__file__)


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }



prev_first_title = ""
FirstRun = True
scraping_site = os.environ.get('PEPPER_SCRAPING_SITE')

while True:
    r = requests.get(scraping_site, headers = headers)
    html_text = r.text
    r_html = HTML(html=html_text)
    prod_class = '.thread-link'
    r_products = r_html.find(prod_class)
    first_prod_title = r_products[0].attrs['title']

    if prev_first_title != first_prod_title:
        if FirstRun == True:
            prev_first_title = first_prod_title
            FirstRun = False
            print ("Zaczynam monitorować "+ scraping_site + " "+ str(datetime.now()))
        else:
            print ("Zanotowano zmiane o: "+ str(datetime.now()) + first_prod_title)
            link = r_products[0].attrs['href']
            prev_first_title = first_prod_title
            obj = Emailer(subject=f"{first_prod_title}", template_html='template.html', context={'offer': first_prod_title, 'link' : link}, to_emails = [os.environ.get('TO_MAIL')], test_send = False)
            obj.send()
    else:
        print('no changes ' + str(datetime.now()))
    time.sleep(10)
    continue

