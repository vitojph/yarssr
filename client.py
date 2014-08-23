#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from requests import get

# first of all, check this
SERVER_URI = 'http://localhost:5001'

app = Flask(__name__)

@app.route('/')
def index():
  '''Generate the page for English RSS'''
  URI = SERVER_URI + '/en'
  result = get(URI).json()
  return render_template('index.html', items=result['items'])

@app.route('/es')
def index_es():
  '''Generate the page for Spanish RSS'''
  URI = SERVER_URI + '/es'
  result = get(URI).json()
  return render_template('index.html', items=result['items'])

@app.route('/about')
def about():
  '''Generate the about page'''
  return render_template('about.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
