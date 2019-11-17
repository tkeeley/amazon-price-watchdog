#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import smtplib
import time

# Request User Input to Set Variables
title = input("What is the name of the item you'd like to watch? ")
url = input("Paste link to Amazon item ")
targetPrice = input("What is your target price? ")
yourEmail = input("What email would you like to send price drop alerts to? ")
URL = url

# Google "what is my user agent" and paste the results between the {""}
headers = {" "}

# Get the title and price of you item
def check_price():
    page = requests.get(URL, headers=headers)

    # Amazon generates the html code with javascript so you have to "trick it"
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    # Your id may be different. Use dev tools to verify the name of the id for the title and price.
    title = soup2.find(id="productTitle").get_text()
    price = soup2.find(id="price_inside_buybox").get_text()
    converted_price = price[0:5]

    if(converted_price < targetPrice):
        send_email()

# Send the email - You can either set up 2 factor auth and generate a specific password or you can turn on less secure apps and use your current gmail email and password
# Must use a gmail email


def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # Replace email and password with your login info
    server.login('email', 'password')

    subject = ('Price Drop for ' + title)
    body = ('Check Amazon ' + URL)

    msg = 'Subject: {}\n\n{}'.format(subject, body)

    # Replace your from email with the email address from above. This is the email your alert will be coming from. The yourEmail variable set globally is the email where you will be recieving your alerts
    server.sendmail(
        'your from email',
        yourEmail,
        msg
    )

    print('Email Has Been Sent')

    server.quit()


# Check every hour for price changes
while(True):
    check_price()
    time.sleep(60 * 60)
