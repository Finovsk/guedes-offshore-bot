import json
import requests
import tweepy
import logging
import os

def get_total():
    quote = requests.get(
        'https://economia.awesomeapi.com.br/json/last/USD-BRL'
    )
    quote_json = json.loads(quote.content)
    total = 9500000*float(quote_json["USDBRL"]["ask"])
    total_currency = "{:,.2f}".format(total)
    logging.info("Total: R${}!".format(total_currency))
    return total_currency


def publish_tweet(consumer_key, consumer_secret, key, secret, total):
    logging.info("Start to publish tweet!")
    
    inicial = 9500000.0 * 3.8595
    rendimento_total = float(total.replace(",","")) - inicial

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)

    api = tweepy.API(auth)
    
    tweets = api.user_timeline(screen_name='guedesoffshore',count=1)
    latest_tweet = str(tweets[0])
    valor = latest_tweet.partition("R$")[2]
    valor = valor.partition("!")[0]
    
    dif = float(total.replace(",","")) - float(valor.replace(",",""))

    if dif > 0:
        logging.info("Setting profit tweet.")
        tweet = "Total R${}!\nEm 02/01/2019, o valor era R${:,.2f}.\nRendeu hoje R${:,.2f}.\nRendimento total R${:,.2f}".format(total, inicial, dif, rendimento_total)
        media = api.media_upload("feliz.jpg")
    else:
        logging.info("Setting loss tweet.")
        tweet = "Total R${}!\nEm 02/01/2019, o valor era R${:,.2f}.\nPerdeu hoje R${:,.2f}.\nRendimento total R${:,.2f}".format(total, inicial, dif, rendimento_total)
        media = api.media_upload("triste.jpg")
    
    #api.update_status(status=tweet, media_ids=[media.media_id])
    print(tweet)

def main():

    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    key = os.environ['KEY']
    secret = os.environ['SECRET']

    logging.basicConfig(level=logging.INFO,format="%(asctime)s:%(levelname)s:%(message)s")

    total = get_total()

    publish_tweet(consumer_key, consumer_secret, key, secret, total)
    logging.info("Tweeted!")

if __name__ == "__main__":
    main()