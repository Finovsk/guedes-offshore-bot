import json
import requests
import tweepy
import os

def get_total():
    quote = requests.get(
        'https://economia.awesomeapi.com.br/json/last/USD-BRL'
    )
    quote_json = json.loads(quote.content)
    total = 9500000*float(quote_json["USDBRL"]["ask"])
    total_currency = "{:,.2f}".format(total)
    return total_currency

def publish_tweet(consumer_key, consumer_secret, key, secret, total):
    # Source http://www.yahii.com.br/dolardiario19.html
    initial = 9500000.0 * 3.8595
    total_revenue = float(total.replace(",","")) - initial
    
    # Authenticate tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)

    # !!!Warning!!! Gambiarra ahead!
    # Set latest total value from latest tweet. (No API found)
    tweets = api.user_timeline(screen_name='guedesoffshore',count=1)
    latest_tweet = str(tweets[0])
    latest_value = latest_tweet.partition("R$")[2]
    latest_value = latest_value.partition("!")[0]

    dif = float(total.replace(",","")) - float(latest_value.replace(",",""))
    if dif > 0:
        tweet = "Total R${}!\nEm 02/01/2019, o valor era R${:,.2f}.\nRendeu hoje R${:,.2f}.\nRendimento total R${:,.2f}.".format(total, initial, dif, total_revenue)
        media = api.media_upload("rendeu.jpg")
    else:
        tweet = "Total R${}!\nEm 02/01/2019, o valor era R${:,.2f}.\nPerdeu hoje R${:,.2f}.\nRendimento total R${:,.2f}.".format(total, initial, dif, total_revenue)
        media = api.media_upload("perdeu.jpg")
    api.update_status(status=tweet, media_ids=[media.media_id])

def main():
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    key = os.environ['KEY']
    secret = os.environ['SECRET']
    total = get_total()
    publish_tweet(consumer_key, consumer_secret, key, secret, total)

if __name__ == "__main__":
    main()