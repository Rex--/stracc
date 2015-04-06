var thisMonth = require(["/web-assets/Chartjs/Chart.min.js", "/web-assets/requirejs/text.js!/web-assets/chart-data/thismonth/linechart.json"], function (Chart, monthdata) {
  var month = JSON.parse(monthdata);
  var maxBs = Math.max.apply(Math, month.chartData);
  var minBs = Math.min.apply(Math, month.chartData);
  var data = {
    labels: month.chartLabels,
    datasets: [
      {
      label: "Diabetes",
      strokeColor: 'rgb(0, 0, 0)',
      data: month.chartData,
      error: [],
      },
      {
      label: "Average",
      strokeColor: 'rgba(0, 0, 255, 0.2)',
      pointColor: 'rgba(0, 0, 0, 0)',
      pointStrokeColor: 'rgba(0, 0, 0, 0)',
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
  dataLength = month.chartLabels.length;
  for(var i = 0; i < dataLength; i++) {
    data.datasets[1].data.push(month.chartDataAvg);
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
  Chart.defaults.global.showTooltips = false;
  var ctx = document.getElementById("chartMain").getContext("2d");
  ctx.canvas.height = window.innerHeight * 0.7;
  ctx.canvas.width = window.innerWidth * 0.7;
  var chart = new Chart(ctx).Line(data, options);
  var disAvg = document.getElementById("chartInfo");
  var chartOpts = document.getElementById("chartOpts");
  disAvg.innerHTML = "<hr><h2 class=\"chartSubTitle\"> This Month's Stats </h2><hr>";
  disAvg.innerHTML += "<p><div class=\"color-box\" id=\"maximum\"></div>Maximum: " + maxBs.toString() + "</p><hr>";
  disAvg.innerHTML += "<p><div class=\"color-box\" id=\"average\"></div>Average: " + month.chartDataAvg.toString() + "</p><hr>";
  disAvg.innerHTML += "<p><div class=\"color-box\" id=\"minimum\"></div>Minimum: " + minBs.toString() + "</p><hr>";
  chartOpts.innerHTML = "<hr><h2 class=\"chartSubTitle\"> Chart Options </h2><hr>";
  chartOpts.innerHTML += "<p> Coming soon! </p><hr>";
});
