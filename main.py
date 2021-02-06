from flask import escape
import tweepy
from tweepy import API
from tweepy import OAuthHandler
from flask import (
    jsonify,
    make_response,
)
from textblob import TextBlob
from googletrans import Translator
from unidecode import unidecode
from flask_api import status as http_status


def getData(request):
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

        # Set CORS headers for the main request
    headers = {
        'Content-Type':'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    request_json = request.get_json(silent=True)
    api_key = 'YOU_API_KEY'
    api_key_secret = 'YOU_KEY_SECRET'
    access_token = 'YOU_ACCESS_TOKEN'
    access_secret = 'YOU_ACCESS_SECRET'
    auth_handler = tweepy.OAuthHandler(consumer_key=api_key, consumer_secret=api_key_secret)
    auth_handler.set_access_token(access_token, access_secret)

    api = tweepy.API(auth_handler)

    search_term = request_json['user']
    tweet_amount = 20
    lang = 'pt'    

    tweets = tweepy.Cursor(api.search, q=search_term, lang=lang).items(tweet_amount)
    
    polarity = 0

    positive = 0
    neutral = 0
    negative = 0
    translator = Translator()

    for tweet in tweets:
        print('for')
        final_text = tweet.text.replace('RT', '')
        if final_text.startswith(' @'):
            position = final_text.index(':')
            final_text = final_text[position+2:]
        if final_text.startswith('@'):
            position = final_text.index(' ')
            final_text = final_text[position+2:]
        #Texto do Tweet
        textPT = unidecode(final_text)
        #Traduzindo para o Inglês
        final_text = translator.translate(textPT)
        analysis = TextBlob(final_text.text)
        tweet_polarity = analysis.polarity
        if tweet_polarity > 0:
            positive += 1
        elif tweet_polarity < 0:
            negative += 1
        else:
            neutral += 1
        polarity += analysis.polarity
    print(polarity)
    print(f'Amount of positives tweets: {positive}')
    print(f'Amount of negatives tweets: {negative}')
    print(f'Amount of neutral tweets: {neutral}')
    response = {
        'status': 1,
        'positive': positive,
        'negative': negative,
        'neutral': neutral,
    }
    return jsonify(response)
