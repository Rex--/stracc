var thisWeek = require(["/web-assets/Chartjs/Chart.min.js", "/web-assets/requirejs/text.js!/web-assets/chart-data/thisweek.json"], function (Chart, weekdata) {

    var data = {
      labels: ["12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
      datasets: [
        {
          label: "Label",
          fillColor: "rgba(220,220,220,0.5)",
          data: ["5", "10", "5", "5", "10", "5", "10", "10", "10", "5", "10", "5"]
        }
      ]
    };
    Chart.defaults.global.showTooltips = false;
    var ctx = document.getElementById("DiabetesChart").getContext("2d");
    ctx.canvas.height = window.innerHeight * 0.5;
    ctx.canvas.width = window.innerWidth * 0.5;
    var chart = new Chart(ctx).Radar(data);
});
