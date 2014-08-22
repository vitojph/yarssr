#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request
from flask.ext.restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)


class ServeResult(Resource):
  items = 'ERROR'
  def get(self, lang):
    if lang == 'en':
      with open('EN.json') as f:
        items = json.load(f)
    elif lang == 'es':
      with open('ES.json') as f:
        items = json.load(f)
    return {'items': items}

api.add_resource(ServeResult, '/<string:lang>')

if __name__ == '__main__':
    app.run(debug=True)
