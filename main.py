import json
import requests
import tweepy
import os


# global variables

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
KEY = os.environ['KEY']
SECRET = os.environ['SECRET']
STARTING_CAPITAL = 9500000
STARTING_CAPITAL_IN_BRL = STARTING_CAPITAL * 3.8595
QUOTE_LINK = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

# methods

def get_total():
    """This function gets actual dollar quote from QUOTE_LINK"""
    
    actual_dolar_quote = requests.get(QUOTE_LINK).content
    quote_json_object = json.loads(actual_dolar_quote)
    value_in_brl = STARTING_CAPITAL * float(quote_json_object["USDBRL"]["ask"])
    formatted_value_in_brl = "{:,.2f}".format(value_in_brl)
    
    return formatted_value_in_brl

def publish_tweet(consumer_key, consumer_secret, key, secret, total):
    """This function publishes a new tweet with gathered data."""
    
    total_revenue = float(total.replace(",","")) - STARTING_CAPITAL_IN_BRL
    
    # Authenticate tweepy access token with Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)

    # !!!Warning!!! Gambiarra ahead! 
    # Set latest total value using data from latest tweet. (No API found, have you thought about using requests with latest tweet link?)

    tweets = api.user_timeline(screen_name='guedesoffshore',count=1)
    latest_tweet = str(tweets[0])
    latest_value = latest_tweet.partition("R$")[2].partition("!")[0]

    difference_from_last_quotation = float(total.replace(",","")) - float(latest_value.replace(",",""))
    
    if difference_from_last_quotation > 0:
        tweet = "Total R${}!\nEm 02/01/2019, o valor era R${:,.2f}.\nRendeu hoje R${:,.2f}.\nRendimento total R${:,.2f}.".format(total, STARTING_CAPITAL_IN_BRL, difference_from_last_quotation, total_revenue)
        media = api.media_upload("rendeu.jpg")
    else:
        tweet = "Total R${}!\nEm 02/01/2019, o valor era R${:,.2f}.\nPerdeu hoje R${:,.2f}.\nRendimento total R${:,.2f}.".format(total, STARTING_CAPITAL_IN_BRL, abs(difference_from_last_quotation), total_revenue)
        media = api.media_upload("perdeu.jpg")
    api.update_status(status=tweet, media_ids=[media.media_id])

def main():
    total = get_total()
    publish_tweet(CONSUMER_KEY, CONSUMER_SECRET, KEY, SECRET, total)

# main

if __name__ == "__main__":
    main()