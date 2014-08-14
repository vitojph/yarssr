#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from pattern.web import Newsfeed, plaintext

# for processing English
from alchemyapi import AlchemyAPI

# for processing Spanish
import urllib
import urllib2
import json
url = 'https://textalytics.com/core/topics'


app = Flask(__name__)
reader = Newsfeed()
alchemyapi = AlchemyAPI()

@app.route('/')
def index():
  RSS_LIST = [
    (u'Lifehacker', 'http://feeds.gawker.com/lifehacker/vip'),
    (u'The Verge', 'http://www.theverge.com/rss/index.xml'),
    (u'Zen Habits', 'http://feeds.feedburner.com/zenhabits?format=xml')
  ]

  items = []

  for feed in RSS_LIST:
    feedlist = []
    for result in reader.search(feed[1])[:10]:
      clean_text = plaintext(result.text)
      response = alchemyapi.entities('text', result.text)

      entities = []
      for entity in response['entities']:
        if entity.has_key('disambiguated'):
          dbpedia_uri = entity['disambiguated']['dbpedia']
        else:
          dbpedia_uri = None
        entities.append((entity['text'], dbpedia_uri))

      feedlist.append(dict(title=result.title, url=result.url, text=clean_text, entities=entities))
    items.append(dict(site=feed[0], feedlist=feedlist))
  return render_template('index.html', items=items)


@app.route('/es')
def index_es():
  RSS_LIST = [
    (u'Menéame', 'http://meneame.feedsportal.com/rss'),
    (u'Naukas', 'http://feeds.feedburner.com/naukas'),
    (u'Yuri', 'http://www.lapizarradeyuri.com/feed/')
  ]

  items = []

  for feed in RSS_LIST:
    feedlist = []
    for result in reader.search(feed[1])[:10]:
      clean_text = plaintext(result.text).encode('utf-8')
      params = urllib.urlencode({
        'key': '4c4ded0a7c279c9f747a8f750e223363', # topic extraction
        'of': 'json',
        'lang': 'es',
        'txt': clean_text,
        'tt': 'a',
        'dm': '5'
      })

      response = json.loads(urllib2.urlopen(url, params).read())

      entities = []
      if response['status']['msg'] == 'OK':
        for e in response['entity_list']:
          if e.has_key('semld_list'):
            for uri in e['semld_list']:
              if 'es.wikipedia' in uri:
                entities.append((e['form'], uri))
                break
              elif 'en.wikipedia' in uri:
                entities.append((e['form'], uri))
              else:
                entities.append((e['form'], None))

      feedlist.append(dict(title=result.title, url=result.url, text=clean_text, entities=entities))
    items.append(dict(site=feed[0], feedlist=feedlist))
  return render_template('index.html', items=items)


@app.route('/about')
def about():
  return render_template('about.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
