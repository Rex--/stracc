var thisMonth = require(["/web-assets/Chartjs/Chart.min.js", "/web-assets/requirejs/text.js!/web-assets/chart-data/thismonth/linechart.json"], function (Chart, monthdata) {
  var month = JSON.parse(monthdata);
  var data = {
    labels: month.chartLabels,
    datasets: [
      {
        label: 'Breakfast',
        strokeColor: 'rgba(210, 210, 0, 0.8)',
        pointColor: 'rgba(210, 210, 0, 1)',
        pointStrokeColor: 'rgba(210, 210, 0, 0)',
        data: month.chartData.Breakfast,
        error: []
      },
      {
        label: 'Lunch',
        strokeColor: 'rgba(85, 107, 47, 0.8)',
        pointColor: 'rgba(85, 107, 47, 1)',
        pointStrokeColor: 'rgba(85, 107, 47, 0)',
        data: month.chartData.Lunch,
        error: []
      },
      {
        label: 'Dinner',
        strokeColor: 'rgba(119, 62, 5, 0.8',
        pointColor: 'rgba(119, 62, 5, 1)',
        pointStrokeColor: 'rgba(119, 62, 5, 0)',
        data: month.chartData.Dinner,
        error: []
      },
      {
        label: 'Bedtime',
        strokeColor: 'rgba(0, 0, 0, 0.8)',
        pointColor: 'rgba(0, 0, 0, 1)',
        pointStrokeColor: 'rgba(0, 0, 0, 0)',
        data: month.chartData.Bedtime,
        error: []
      }
    ]
  };
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
  chartOpts.innerHTML = "<hr><h2 class=\"chartSubTitle\"> Time of Day </h2><hr>";
  chartOpts.innerHTML += "<p><div class=\"color-box\" id=\"breakfast\"></div> Breakfast </p><hr>";
  chartOpts.innerHTML += "<p><div class=\"color-box\" id=\"lunch\"></div> Lunch </p><hr>";
  chartOpts.innerHTML += "<p><div class=\"color-box\" id=\"dinner\"></div> Dinner </p><hr>";
  chartOpts.innerHTML += "<p><div class=\"color-box\" id=\"bedtime\"></div> Bedtime </p>";
  disAvg.innerHTML = "<hr><h2 class=\"chartSubTitle\"> This Month's Stats </h2><hr>";
  disAvg.innerHTML += "<p><div class=\"color-box\" id=\"average\"></div>Average: </p><hr>";
});
