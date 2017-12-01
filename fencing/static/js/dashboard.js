// -- Area Chart Example
var ctx;
var projectNames;
var projectProfit;

function getProfits(){
  $.ajax({
    type: 'GET',
    url: '/getProfit/',
    success: function(result) {
      console.log(result);
      projectProfit = result["profits"];
      projectNames = result["projects"];
      makeChart();
    },
    error: function(result) {
        showMessage("Error getting material lists");
    }
  });
}


$(document).ready(function(){
  ctx = document.getElementById("myChart");
  getProfits();
})

function makeChart(){
  var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: projectNames,
      datasets: [{
        label: "Sessions",
        yAxisID: 'y-axis-0',
        lineTension: 0.3,
        backgroundColor: "rgba(25,200,25,0.2)",
        borderColor: "rgba(2,117,216,1)",
        pointRadius: 5,
        pointBackgroundColor: "rgba(2,117,216,1)",
        pointBorderColor: "rgba(255,255,255,0.8)",
        pointHoverRadius: 5,
        pointHoverBackgroundColor: "rgba(2,117,216,1)",
        pointHitRadius: 20,
        pointBorderWidth: 2,
        data: projectProfit,
      }],
    },
    options: {
      scales: {
        xAxes: [{
          time: {
            unit: 'date'
          },
          gridLines: {
            display: false
          },
          ticks: {
            maxTicksLimit: 7
          }
        }],
        yAxes: [{
          ticks: {
            beginAtZero: true,
            maxTicksLimit: 5
          },
          gridLines: {
            color: "rgba(0, 0, 0, .125)",
          }
        }],
      },
      legend: {
        display: false
      }
    }
  });
}
