from datetime import datetime
from send_mail import Emailer
from requests_html import HTMLSession
import os
import time

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

session = HTMLSession()

headers = {
    '''User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36
         (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36`''',
}


prev_first_title = ""

FirstRun = True

link = os.environ.get('PEPPER_SCRAPING_SITE')


my_list = [
    'nintendo', 'lego'
]

while True:
    r = session.get(link)
    # finding first product and its title
    first_prod = r.html.find('.cept-tt', first=True)
    price = r.html.find(
        '.thread-price.text--b.cept-tp.size--all-l.size--fromW3-xl', first=True).text
    first_prod_title = first_prod.attrs['title']
    print(f'{first_prod_title} za {price}')

    # if there is a new product, check if its in the list
    if prev_first_title != first_prod_title:
        if FirstRun:
            prev_first_title = first_prod_title
            FirstRun = False
            print("Zaczynam monitorować " + link
                  + " " + str(datetime.now()))
        else:
            print("Zanotowano zmiane o: " +
                  str(datetime.now()) + first_prod_title)

            for item in my_list:

                title_lowercase = first_prod_title.casefold()

                if item in title_lowercase:
                    print(f"Found {item} in the title!")
                    first_prod_link = first_prod.attrs['href']

                    # sending email with product that matches our preferences

                    obj = Emailer(
                        subject=f"{first_prod_title}",
                                template_html='template.html',
                        context={
                            'offer': first_prod_title, 'link': first_prod_link, 'price': price},
                        to_emails=[os.environ.get('TO_MAIL')],
                        test_send=False)

                    obj.send()

                    print(f'wysłano mail z {item}')

            prev_first_title = first_prod_title

    time.sleep(20)
    continue
