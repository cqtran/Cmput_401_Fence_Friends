// -- Area Chart Example
var ctx = document.getElementById("myChart");
var projectNames = ["test", "tw", "gre"];
var projectProfit = [100, 400030, -10000];
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