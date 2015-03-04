

require(["web-assets/Chartjs/Chart.min.js", "requirejs/text!bloodsugars.json"], function (Chart, bloodsugars) {

  var sugarDB = JSON.parse(bloodsugars);
  var sugarTable = sugarDB.results;

  var data = {
    labels: [],
    datasets: [
      {
      label: "Diabetes",
      strokeColor: 'rgb(0, 0, 0)',
      data: []
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

  for(var i = 0; i < sugarTable.length; i++) {
      var bloodsugar = parseInt(sugarTable[i]['bloodsugar']);
      var time = sugarTable[i]['time'];
      // add time datapoint to the chart
      data.labels.push(time);
      // add blood sugar datapoint to the chart
      data.datasets[0].data.push(bloodsugar);
  }

  var ctx = document.getElementById("DiabetesChart").getContext("2d");
  ctx.canvas.height = window.innerHeight / 2;
  ctx.canvas.width = window.innerWidth / 2;
  var chart = new Chart(ctx).Line(data, options);

});
