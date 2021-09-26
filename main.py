

import requests, os
from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
from collections import Counter
from dotenv import load_dotenv
import pya3rt

#envファイルの読み込み
load_dotenv()

A3RT_API_KEY = os.environ['A3RT_API_KEY']
client = pya3rt.TalkClient(A3RT_API_KEY)

if __name__ == '__main__':
  words = input("あなた >")
  while words!="":
    response = client.talk(words)
    print("Bot >"+((response['results'])[0])['reply'])
    words = input("あなた >")
