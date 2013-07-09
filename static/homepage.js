$(window).load(function() {
	var $windowHeight = $(window).height() - 50;
	$('h1').css({'margin-top' : (($windowHeight) - $('h1').outerHeight())/2,'margin-bottom' : (($windowHeight) - $('h1').outerHeight())/2,'opacity' : '1.0','filter' : 'alpha(opacity = 100)',});
	drawChart();
});

// time is the resolution of the graph, in seconds
    // larger numbers make smoother graphs
    var time = 600;
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
        counts.push(0);
        for (var i = 0; i < arr.length; i++) {
          if (arr[i] == x) {
            counts[counts.length-1]++;
          }
        }
      }
      return counts;
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
        $('.dynamicsparkline').sparkline(counts, {width: '800', height: '200'});

        // generate labels based on current time
        var tds = (new Date()).getHours() + 1;
        $("table td").each(function () {
          $(this).html(pad(tds,2));
          tds += 1;
          if (tds == 24) {tds = 0}
        });
      });
    };


window.setInterval(function(){$.getJSON('http://librarycounter/api/count/today',function(data){$('h1').text(data);}); drawChart();},5000);