import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import argparse


def shorten_link(token, link):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    response = requests.post(url, headers={'Authorization': token}, 
                             json={'long_url': link})
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, bitlink): 
    parsed = urlparse(bitlink)
    url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(parsed.netloc + parsed.path)
    response = requests.get(url, headers={'Authorization': token})
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(token, link):
    try:
        parsed = urlparse(link)
        url = 'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(parsed.netloc + parsed.path)
        response = requests.get(url, headers={'Authorization': token})
        response.raise_for_status()
        is_bitlink = True
    except requests.exceptions.HTTPError:
        is_bitlink = False
    return is_bitlink

if __name__ == '__main__':
    load_dotenv()
    token = os.getenv("BITLY_AUTHORIZATION_TOKEN")
    parser = argparse.ArgumentParser()
    parser.add_argument('link', help='Введите ссылку')
    args = parser.parse_args()
    link = args.link
    if is_bitlink(token, link):
	    try:
	        print('Количество переходов по битлинку:', count_clicks(token, link))
	    except requests.exceptions.HTTPError:
	        print('Неверная ссылка!')
    else:
	    try:
	        bitlink = shorten_link(token, link)
	        print('Битлинк', bitlink)
	    except requests.exceptions.HTTPError:
	        print('Неверная ссылка')




     


