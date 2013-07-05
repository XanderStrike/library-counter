#server.py
# Serves information for the api and the web page

from bottle import hook, response, route, run, template
import sqlite3 as lite
import sys
import time
import json

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

con = lite.connect('db')

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
@route('/api/<period>.json')
def api(period='day'):
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
    cur.execute("SELECT * FROM Times")
    return json.dumps(cur.fetchall())
  
  cur.execute("SELECT * FROM Times WHERE Time > " + str(time.time() - mod))
  return json.dumps(cur.fetchall())

@route('/')
def index():
  cur = con.cursor()
  cur.execute("SELECT COUNT(*) FROM Times WHERE Time > " + (str((time.time() - (time.time() % 86400))+25200)))
  count = cur.fetchall()[0][0]
  return template('''
<html><head><title>Library Count</title><link href='http://fonts.googleapis.com/css?family=Advent+Pro:400,300' rel='stylesheet' type='text/css'><style>body {margin:0px 0px 0px 0px;}#main {background:url(http://24.media.tumblr.com/tumblr_linam9F4Tg1qz6s22o1_1280.jpg);background-size:cover;background-position:center bottom;}.inner {background: rgba(0,0,0,0.2) url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAACp8Z5+AAAAGklEQVQIW2NkYGD4D8SMQAwGcAY2AbBKDBUAVuYCBQPd34sAAAAASUVORK5CYII=) repeat;padding:10px 10px;color:#eee;min-height: calc(100% - 20px);}h1 {font-family: 'Advent Pro', sans-serif;font-size:200px;text-align:center;}</style><script src="http://code.jquery.com/jquery-1.10.1.min.js"></script><script>$(window).load(function() {var $windowHeight = $(window).height() - 50;$('h1').css({'margin-top' : (($windowHeight) - $('h1').outerHeight())/2,'margin-bottom' : (($windowHeight) - $('h1').outerHeight())/2,'opacity' : '1.0','filter' : 'alpha(opacity = 100)',});});</script></head><body>  <section id="main">    <div class="inner"><h1>{{output}}</h1></div></section><script>window.setInterval(function(){$.getJSON('http://10.23.4.112/api/count/today',function(data){$('h1').text(data);});},2500);</script></body></html>
''', output=count)

run(host='0.0.0.0', port=80)
