require(["/web-assets/Chartjs/Chart.min.js", "/web-assets/requirejs/text!/web-assets/chart-data/alltime.json"], function (Chart, allData) {
  var alltime = JSON.parse(allData);
  var data = {
    labels: alltime.chartLabels,
    datasets: [
      {
      label: "Diabetes",
      strokeColor: 'rgb(0, 0, 0)',
      data: alltime.chartData,
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
  var ctx = document.getElementById("DiabetesChart").getContext("2d");
  ctx.canvas.height = window.innerHeight * 0.7;
  ctx.canvas.width = window.innerWidth * 0.7;
  var chart = new Chart(ctx).Line(data, options);
});
