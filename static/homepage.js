// homepage.js
// Javascript for the homepage.
//   Contains functions both for the automatic updating of the large counter and
//   the drawing of the graph
//
// Alex Standke

$(window).load(function() {
	var $windowHeight = $(window).height()-600;
	$('h1').css({'margin-top' : (($windowHeight) - $('h1').outerHeight())/2,'opacity' : '1.0','filter' : 'alpha(opacity = 100)',});
	drawChart();
});

// time is the resolution of the graph, in seconds
// larger numbers make smoother graphs
var time = 900;
var timeNow = Math.round(new Date().getTime() / 1000)
var time24HoursAgo = (timeNow - (timeNow % time)) - 86400

// pad numbers with zeros to size
function pad(num, size) {
  var s = num+"";
  while (s.length < size) s = "0" + s;
  return s;
}

// get count at each time between the start and end of the data
function getCounts(arr) {
  var counts = []
  for (var x=time24HoursAgo; x < timeNow; x+=time) {
    counts.push([x, 0]);
      for (var i = 0; i < arr.length; i++) {
        if (arr[i] == x) {
          counts[counts.length-1][1]++;
        }
      }
  }
  return counts;
}

// turn integer time into human readable
function to_time(int_time) {
  var date = new Date(int_time * 1000)
  var hh = date.getHours();
  var mm = date.getMinutes();

  if (hh > 12) {ampm = "pm"} else {ampm = "am"}
  if (hh == 0) {hh = 12;}
  if (hh > 12) {hh = hh - 12;}

  return hh+":"+pad(mm, 2)+ampm
}

// actual function called on page load
function drawChart()  {
  $.getJSON('http://librarycounter/api/day', function(data) {
    // build arr to have just integer times
    var arr = [];
    $.each(data, function(d) {
      arr.push(data[d][0] - (data[d][0] % time));
    });

    // assemble array with counts for each <time> interval
    var counts = getCounts(arr);

    // build sparkline
    $.plot('#graph', 
            [counts],
            {
              xaxis: {
                tickFormatter: to_time
              },
              lines: {
                fill: true
              }
            });

    // generate labels based on current time
    var tds = (new Date()).getHours() + 1;
    $("table td").each(function () {
      $(this).html(pad(tds,2));
      tds += 1;
      if (tds == 24) {tds = 0}
    });
  });
};

function update() {
  $.getJSON('http://librarycounter/api/count/today',function(data){$('h1').text(data);});
  drawChart();
}

window.setInterval(function(){update();},5000);

