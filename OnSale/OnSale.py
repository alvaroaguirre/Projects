########## On sale ##########
# Alvaro Aguirre - Nov 6th

# This Python script goes into a product page, checks if the selling price has decreased, and sends an email if so

# Libraries
import requests
from bs4 import BeautifulSoup
import smtplib, ssl

# Access the page and use BeautifulSoup's html.parser
page = requests.get("https://www.coffeedesk.com/product/8558/Fellow-Stagg-Ekg-Electric-Pour-Over-Kettle-Matte-Black")
soup = BeautifulSoup(page.content, 'html.parser')
# Use the product-price class to find the current price, and format it into float
price = float(soup.find('span', class_ = 'product-price').text.split(" ")[0].replace(",","."))

# Prepare email details
port = 465
smtp_server = "smtp.gmail.com"
sender_email = "Enter the sender email here"
receiver_email = "Receiver email here"
password = "Your password"
message = """\
Subject: Fellow EKG for sale!

Hi Alvaro, 

This is Alvaro from the past.
If you are getting this, it means that the Fellow EKG is on sale on Coffeedesk.
The new price is """ + str(price) +""" euros.
Here is the link in case you want to get it:

https://www.coffeedesk.com/product/8558/Fellow-Stagg-Ekg-Electric-Pour-Over-Kettle-Matte-Black

Hopefully it's a good deal!

Cheers,
Alvaro
"""

context = ssl.create_default_context()

# Send the email if the price is lower than retail price
if price < 166:
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)