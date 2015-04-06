var thisWeek = require(["/web-assets/Chartjs/Chart.min.js", "/web-assets/requirejs/text.js!/web-assets/chart-data/thisweek/linechart.json"], function (Chart, weekdata) {
  var week = JSON.parse(weekdata);
  var maxBs = Math.max.apply(Math, week.chartData);
  var minBs = Math.min.apply(Math, week.chartData);
  var data = {
    labels: week.chartLabels,
    datasets: [
      {
      label: "Diabetes",
      strokeColor: 'rgb(0, 0, 0)',
      data: week.chartData,
      error: [],
      },
      {
      label: "Average",
      strokeColor: 'rgba(0, 0, 255, 0.2)',
      pointColor: 'rgba(0, 0, 0, 0)',
      pointStrokeColor: 'rgba(0, 0, 0, 0)',
      fillColor: 'rgba(0, 0, 255, 0.5)',
      data : [],
      error: []
      },
      {
      label: "Maximum",
      strokeColor: 'rgba(255, 0, 0, 0.2)',
      pointColor: 'rgba(0, 0, 0, 0)',
      pointStrokeColor: 'rgba(0, 0, 0, 0)',
      data: [],
      error: []
      },
      {
      label: "Minimum",
      strokeColor: 'rgba(0, 255, 0, 0.3)',
      pointColor: 'rgba(0, 0, 0, 0)',
      pointStrokeColor: 'rgba(0, 0, 0, 0)',
      data: [],
      error: []
      }
    ]
  };
  dataLength = week.chartLabels.length;
  for(var i = 0; i < dataLength; i++) {
    data.datasets[1].data.push(week.chartDataAvg);
    data.datasets[2].data.push(maxBs);
    data.datasets[3].data.push(minBs);
  }
  var options = {
          scaleBeginAtZero: false,
          scaleShowVerticalLines: true,
          bezierCurve: true,
          datasetFill: false,
          pointDot: true,
          datasetStrokeWidth: 2,
  };
  //Chart.defaults.global.showTooltips = false;
  var ctx = document.getElementById("chartMain").getContext("2d");
  ctx.canvas.height = window.innerHeight * 0.7;
  ctx.canvas.width = window.innerWidth * 0.7;
  var chart = new Chart(ctx).Line(data, options);
  var disAvg = document.getElementById("chartInfo");
  var chartOpts = document.getElementById("chartOpts");
  chartOpts.innerHTML = "<hr><h2 class=\"chartSubTitle\"> Time of Day </h2><hr>";
  chartOpts.innerHTML += "<p><div class=\"color-box\" id=\"breakfast\"></div> Breakfast </p><hr>";
  chartOpts.innerHTML += "<p><div class=\"color-box\" id=\"lunch\"></div> Lunch </p><hr>";
  chartOpts.innerHTML += "<p><div class=\"color-box\" id=\"dinner\"></div> Dinner </p><hr>";
  chartOpts.innerHTML += "<p><div class=\"color-box\" id=\"bedtime\"></div> Bedtime </p>";
  disAvg.innerHTML = "<hr><h2 class=\"chartSubTitle\"> This Week's Stats </h2><hr>";
  disAvg.innerHTML += "<p><div class=\"color-box\" id=\"maximum\"></div>Maximum: " + maxBs.toString() + "</p><hr>";
  disAvg.innerHTML += "<p><div class=\"color-box\" id=\"average\"></div>Average: " + week.chartDataAvg.toString() + "</p><hr>";
  disAvg.innerHTML += "<p><div class=\"color-box\" id=\"minimum\"></div>Minimum: " + minBs.toString() + "</p><hr>";
});
