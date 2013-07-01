from bottle import route, run, template

@route('/hello/<name>')
def index(name='World'):
  return template('''
<html>
<head>
  <title>This is a page.</title>
  <style>body {margin:0px 0px 0px 0px;}#main {background:url(http://24.media.tumblr.com/tumblr_linam9F4Tg1qz6s22o1_1280.jpg);background-size:cover;background-position:center bottom;} .inner {background: rgba(0,0,0,0.2) url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAACp8Z5+AAAAGklEQVQIW2NkYGD4D8SMQAwGcAY2AbBKDBUAVuYCBQPd34sAAAAASUVORK5CYII=) repeat; padding:10px 10px;  color:#eee;  min-height: calc(100% - 20px);}
</style>
</head>
<body>
  <section id="main">
    <div class="inner">
 	{{name}}   lolwut 
    </div>
  </section>
</body>
</html>
''', name=name)

run(host='0.0.0.0', port=8080)
