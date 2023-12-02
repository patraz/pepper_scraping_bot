from datetime import datetime
from send_mail import Emailer
# from dotenv import load_dotenv
from requests_html import HTMLSession
import os
import time

from dotenv import load_dotenv


load_dotenv()


session = HTMLSession()


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }

prev_first_title = ""
FirstRun = True
scraping_site = os.environ['PEPPER_SCRAPING_SITE']
my_list = ['piżama', 'ps4', 'nintendo', 'm&m', 'kucharska', 'nawilżacz', 'puzzle', 'air fryer']
print('DUPAAAAAAAAAA')
while True:
    r = session.get('https://www.pepper.pl/gorące')
    first_prod = r.html.find('.cept-tt', first=True)
    first_prod_title = first_prod.attrs['title']
    print(first_prod_title)

    
    if prev_first_title != first_prod_title:
        if FirstRun == True:
            prev_first_title = first_prod_title
            FirstRun = False
            print ("Zaczynam monitorować "+ scraping_site + " "+ str(datetime.now()))
        else:
            print ("Zanotowano zmiane o: "+ str(datetime.now()) + first_prod_title)
            for item in my_list:
                if item in first_prod_title:
                    # Do something if there's a match
                    print(f"Found {item} in the title!")
                    first_prod_link = first_prod.attrs['href']
                    obj = Emailer(subject=f"{first_prod_title}", template_html='template.html', context={'offer': first_prod_title, 'link' : first_prod_link}, to_emails = [os.environ.get('TO_MAIL')], test_send = False)
                    obj.send()
            prev_first_title = first_prod_title
    else:
        print('no changes ' + str(datetime.now()))
    time.sleep(60)
    continue

