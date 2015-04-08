var thisToday = require(["/web-assets/Chartjs/Chart.min.js", "/web-assets/requirejs/text.js!/web-assets/chart-data/today/radarchart.json"], function (Chart, radardata) {
    var today = JSON.parse(radardata);
    var padding = Math.ceil(today.bloodsugarHigh/100)*100;
    var highData = [];
    for(var i = 0; i < 4; i++) {
      highData.push(padding);
    }

    var data = {
      labels: ["Breakfast", "Lunch", "Dinner", "Bedtime"],
      datasets: [
        {
          label: "HighBloodsugars",
          fillColor: "rgba(255, 0, 0, 0.1)",
          strokeColor: "rgba(255, 0, 0, 0.2)",
          pointColor: "rgba(255, 0, 0, 0)",
          pointStrokeColor: "rgba(255, 0, 0, 0)",
          data: highData
        },
        {
          label: "GoodBloodsugars",
          fillColor: "rgba(0, 255, 0, 0.1)",
          strokeColor: "rgba(255, 0, 0, 0.2)",
          pointColor: "rgba(0, 255, 0, 0)",
          pointStrokeColor: "rgba(0, 255, 0, 0)",
          data: [130, 130, 130, 150]
        },
        {
          label: "LowBloodsugars",
          fillColor: "rgba(255, 0, 0, 0.1)",
          strokeColor: "rgba(255, 0, 0, 0.2)",
          pointColor: "rgba(255, 0, 0, 0)",
          pointStrokeColor: "rgba(255, 0, 0, 0)",
          data: [70, 70, 70, 80]
        },
        {
          label: "BloodsugarData",
          fillColor: "rgba(0, 0, 0, 0)",
          strokeColor: "rgba(0, 0, 0, 0.4)",
          pointColor: "rgba(0, 0, 0, 1)",
          pointStrokeColor: "rgba(0, 0, 0, 0)",
          data: today.bloodsugarData
        }
      ]
    };
    options = {
      pointLabelFontSize: 16
    };
    Chart.defaults.global.showTooltips = false;
    var ctx = document.getElementById("todayChart").getContext("2d");
    ctx.canvas.height = window.innerHeight * 0.5;
    ctx.canvas.width = window.innerWidth * 0.5;
    var chart = new Chart(ctx).Radar(data, options);
    var tInfo = document.getElementById("todayInfo");
    tInfo.innerHTML = "<hr><h2 class=\"chartSubTitle\" id=\"breakfast\">Breakfast: " + today.bloodsugarData[0].toString() + "</h2><hr>";
    tInfo.innerHTML += "<h2 class=\"chartSubTitle\" id=\"lunch\">Lunch: " + today.bloodsugarData[1].toString() + "</h2><hr>";
    tInfo.innerHTML += "<h2 class=\"chartSubTitle\" id=\"dinner\">Dinner: " + today.bloodsugarData[2].toString() + "</h2><hr>";
    tInfo.innerHTML += "<h2 class=\"chartSubTitle\" id=\"bedtime\">Bedtime: " + today.bloodsugarData[3].toString() + "</h2><hr>"; 
});
