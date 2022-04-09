import json
import requests
import tweepy
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
import base64
from babel.numbers import format_decimal

# global
# github secrets and json <3
CREDENTIALS = base64.b64decode(os.environ['CREDENTIALS'])
CREDENTIALS = CREDENTIALS.decode('ascii')
CREDENTIALS = json.loads(CREDENTIALS)

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
KEY = os.environ['KEY']
SECRET = os.environ['SECRET']
SCOPE = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
STARTING_CAPITAL = 9500000
STARTING_CAPITAL_IN_BRL = STARTING_CAPITAL * 3.8595
QUOTE_LINK = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

# methods

def get_quote():
    """This function gets actual dollar quote from QUOTE_LINK"""
    
    dolar_quote = requests.get(QUOTE_LINK, headers={"Cache-Control": "no-cache"}).content
    dolar_quote = json.loads(dolar_quote)
    dolar_quote = float(dolar_quote["USD"]["ask"])
    return dolar_quote

def get_total():
    """This function gets total value on account"""
    
    dolar_quote = get_quote()
    value_in_brl = STARTING_CAPITAL * dolar_quote
    return value_in_brl

def publish_tweet(consumer_key, consumer_secret, key, secret, credentials, scope):
    """This function publishes a new tweet with gathered data."""
    
    dolar_quote = get_quote()
    total = get_total()
    total_revenue = total - STARTING_CAPITAL_IN_BRL
    
    # Authenticate tweepy access token with Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)

    # Authenticate Google Drive
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
    client = gspread.authorize(creds)
    sheet = client.open("total").sheet1
    
    # Get previous total value from sheet
    previous_total_value = float(sheet.cell(2, 2).value)

    # Save latest value
    today = str(date.today())
    new_row = [today, total, dolar_quote]
    sheet.insert_row(new_row, 2)

    difference_from_last_total = total - previous_total_value

    # Set variables for BR readers
    locale_dolar_quote = format_decimal(dolar_quote, locale='pt_BR')
    locale_total = format_decimal(total, locale='pt_BR')
    locale_starting = format_decimal(STARTING_CAPITAL_IN_BRL, locale='pt_BR')
    locale_difference = format_decimal(abs(difference_from_last_total), locale='pt_BR')
    locale_revenue = format_decimal(total_revenue, locale='pt_BR')
    
    if difference_from_last_total > 0:
        tweet = "Dólar hoje: R${}.\nTotal na conta do véio: R${}!\nEm 02/01/2019, o valor era R${}.\nRendeu hoje R${}.\nRendimento total R${}.".format(locale_dolar_quote, locale_total, locale_starting, locale_difference, locale_revenue)
        media = api.media_upload("rendeu.jpg")
    else:
        tweet = "Dólar hoje: R${}.\nTotal na conta do véio: R${}!\nEm 02/01/2019, o valor era R${}.\nPerdeu hoje R${}.\nRendimento total R${}.".format(locale_dolar_quote, locale_total, locale_starting, locale_difference, locale_revenue)
        media = api.media_upload("perdeu.jpg")
    api.update_status(status=tweet, media_ids=[media.media_id])

def main():
    publish_tweet(CONSUMER_KEY, CONSUMER_SECRET, KEY, SECRET, CREDENTIALS, SCOPE)
    
# main

if __name__ == "__main__":
    main()
