#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import json

SENTENCE = '''La UE teme que Hungría alimente la tentación totalitaria de Europa. El país gobernado por Viktor Orbán es el primer socio de los Veintiocho que defiende un modelo de libertades recortadas desde 1998. Ha perdido más de 28 millones de euros desde hace una década.'''

#SENTENCE = u'''The cat is on the nap. Ms Black is here right back.'''

# Send the GET request
url = 'https://textalytics.com/core/topics'
params = urllib.urlencode({
  'key': '4c4ded0a7c279c9f747a8f750e223363', # semantic publishing
  'of': 'json',
  'lang': 'es',
  'txt': SENTENCE,
  'tt': 'a',
  'dm': '5'
})

response = json.loads(urllib2.urlopen(url, params).read())

if response['status']['msg'] == 'OK':
  for e in response['entity_list']:
    print e['form'], e['sementity']['type'],
    if e.has_key('semld_list'):
      for uri in e['semld_list']:
        if 'en.wikipedia' in uri:
          print uri
    else:
      print

  for m in response['money_expression_list']:
    print m['form'], m['amount'], m['numeric_value'], m['currency']
