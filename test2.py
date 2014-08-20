#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import json
from pattern.web import Newsfeed, plaintext

reader = Newsfeed()

RSS_LIST = [
  (u'Menéame', 'http://meneame.feedsportal.com/rss'),
  (u'Naukas', 'http://feeds.feedburner.com/naukas'),
  (u'Yuri', 'http://www.lapizarradeyuri.com/feed/')
]

url = 'https://textalytics.com/core/topics'

items = []

print '-------------------------------'
for feed in RSS_LIST:
  print 'feed'
  feedlist = []
  for result in reader.search(feed[1])[:10]:
    clean_text = plaintext(result.text).encode('utf-8')

    try:
      params = urllib.urlencode({
        'key': '4c4ded0a7c279c9f747a8f750e223363', # topic extraction
        'of': 'json',
        'lang': 'es',
        'txt': clean_text,
        'tt': 'a',
        'dm': '5'
      })
    except UnicodeEncodeError:
      raise

    response = json.loads(urllib2.urlopen(url, params).read())

    entities = []
    if response['status']['msg'] == 'OK':
      for e in response['entity_list']:
        if e.has_key('semld_list'):
          for uri in e['semld_list']:
            if 'es.wikipedia' in uri:
              entities.append((e['form'], uri))
              break

    feedlist.append(dict(title=result.title, url=result.url, text='', entities=entities))
  items.append(dict(site=feed[0], feedlist=feedlist))

  print items
