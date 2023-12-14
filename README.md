# pepper_scraping_bot

Bot that sends you e-mail when new listing on pepper contains one of your preferences 

Just add .env file with

smtp credintials

USERNAME = 
PASSWORD = 

PEPPER_SCRAPING_SITE = https://www.pepper.pl/nowe - or other url of pepper.pl

TO_MAIL= mail where bot will send new listings on PEPPER_SCRAPING_SITE

edit send_mail.py according to your smtp provider

and edit pepper.py to your needs 
for example

my_list = ['game', 'ps4', 'laptop']

