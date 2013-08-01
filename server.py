#server.py
# Serves information for the api and the web page

from lib.bottle import hook, response, route, run, template, static_file
import sqlite3 as lite
import sys
import time
import json

con = lite.connect('db/data.sqlite3')

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/api/count/<period>')
@route('/api/count/<period>.json')
def api_count(period='today'):
  cur = con.cursor()
  mod = 1
  if period == 'hour':
    mod = 3600
  elif period == 'day':
    mod = 86400
  elif period == 'week':
    mod = 604800
  elif period == 'month':
    mod = 2592000
  elif period == 'year':
    mod = 31536000
  elif period == 'all':
    cur.execute("SELECT COUNT(*) FROM Times")
    return str(cur.fetchall()[0][0])
  elif period == 'today':
    cur.execute("SELECT COUNT(*) FROM Times WHERE Time > " + (str((time.time() - (time.time() % 86400))+25200))) 
    return str(cur.fetchall()[0][0])

  cur.execute("SELECT COUNT(*) FROM Times WHERE Time > " + str(time.time() - mod))
  return str(cur.fetchall()[0][0])

@route('/api/<period>')
@route('/api/<period>/<value>')
@route('/api/<period>.json')
def api(period='day', value=24):
  cur = con.cursor()
  mod = 1
  if period == 'hour':
    mod = 3600
  elif period == 'day':
    mod = 86400
  elif period == 'week':
    mod = 604800
  elif period == 'month':
    mod = 2592000
  elif period == 'year':
    mod = 31536000
  elif period == 'hours':
    mod = 3600 * int(value)
  elif period == 'all':
    cur.execute("SELECT * FROM Times")
    return json.dumps(cur.fetchall())
  
  cur.execute("SELECT * FROM Times WHERE Time > " + str(time.time() - mod))
  return json.dumps(cur.fetchall())

@route('/graph')
def graph():
  return static_file('graph.html', root='./static/')

@route('/customgraph')
def graph():
  return static_file('customgraph.html', root='./static/')

@route('/')
def index():
  cur = con.cursor()
  cur.execute("SELECT COUNT(*) FROM Times WHERE Time > " + (str((time.time() - (time.time() % 86400))+25200)))
  count = cur.fetchall()[0][0]
  return template('''
<html><head><title>Library Count</title><link href='http://fonts.googleapis.com/css?family=Advent+Pro:400,300' rel='stylesheet' type='text/css'><link href="/static/homestyle.css" rel='stylesheet' type='text/css'><script src="/static/jquery-1.10.1.min.js"></script><script src="/static/jquery.sparkline.min.js"></script><script src="/static/homepage.js"></script></head><body><section id="main"><div class="inner"><h1>{{output}}</h1></div></section><center><br><br><span class="dynamicsparkline">Loading...</span><br><table width=800 style='font-family: monospace;color:#aaa;'><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td width=1%></td></tr></table></center><script>window.onload = function() {document.body.className += ' loaded'};</script></body></html>
''', output=count)

# for any files in static/
@route('/static/:filename')
def send_static(filename):
  return static_file(filename, root='./static/')

run(host='0.0.0.0', port=80)
