#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pattern.web import Newsfeed, plaintext
# for processing English
from alchemyapi import AlchemyAPI
# for processing Spanish
import urllib
import urllib2
import json
url = 'https://textalytics.com/core/topics'

reader = Newsfeed()
alchemyapi = AlchemyAPI()

def process_EN():
  '''Processes the English RSS feeds, locate entities and returns a list of tuples URI, DICT, where DICT contains entry's title, URL, plain text and list of entities.'''
  EN_RSS_LIST = [
    (u'Lifehacker', 'http://feeds.gawker.com/lifehacker/vip'),
    (u'The Verge', 'http://www.theverge.com/rss/index.xml'),
    (u'Zen Habits', 'http://feeds.feedburner.com/zenhabits?format=xml')
    ]
  items = []
  for feed in EN_RSS_LIST:
    feedlist = []
    # fetch the feed
    for result in reader.search(feed[1])[:10]:
      clean_text = plaintext(result.text)
      response = alchemyapi.entities('text', result.text)
      # parse the entities
      entities = []
      for entity in response['entities']:
        if entity.has_key('disambiguated'):
          dbpedia_uri = entity['disambiguated']['dbpedia']
        else:
          dbpedia_uri = None
        entities.append((entity['text'], dbpedia_uri))

      feedlist.append(dict(title=result.title, url=result.url, text=clean_text, entities=entities))
    items.append(dict(site=feed[0], feedlist=feedlist))
  return items


def process_ES():
  '''Processes the Spanish RSS feeds, locate entities and returns a list of tuples URI, DICT, where DICT contains entry's title, URL, plain text and list of entities.'''
  ES_RSS_LIST = [
    (u'Menéame', 'http://meneame.feedsportal.com/rss'),
    (u'Naukas', 'http://feeds.feedburner.com/naukas'),
#    (u'Yuri', 'http://www.lapizarradeyuri.com/feed/')
  ]
  items = []
  # fetch the feed
  for feed in ES_RSS_LIST:
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
      # parse the entities
      entities = []
      if response['status']['msg'] == 'OK':
        for e in response['entity_list']:
          if e.has_key('semld_list'):
            for uri in e['semld_list']:
              if 'es.wikipedia' in uri:
                entities.append((e['form'], uri))
                break

      feedlist.append(dict(title=result.title, url=result.url, text=clean_text, entities=entities))
    items.append(dict(site=feed[0], feedlist=feedlist))
    return items


if __name__ == '__main__':
  with open('EN.json', 'w') as f:
    f.write(json.dumps(process_EN()))

  with open('ES.json', 'w') as f:
    f.write(json.dumps(process_ES()))
