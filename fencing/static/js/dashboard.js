// -- Area Chart Example
var ctx;
var projectNames;
var projectProfit;

//sends an http request to return profit values
function getProfits(){
  $.ajax({
    type: 'POST',
    url: '/getProfit/',
    data: {'year': $('#year').val()},
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

// generate list of years
function yearSelect(){
  for (i = new Date().getFullYear(); i > 2015; i--) {
    $('select[name=year]').append('<option value="' + i + '">' + i + '</option>');
  }
  $('.selectpicker').selectpicker('refresh');
}

//runs after document loads
$(document).ready(function(){
  yearSelect();
  ctx = document.getElementById("myChart");
  getProfits();

  $('#year').on('change', function() {
    getProfits();
  });
});

//creates the line graph
function makeChart(){
  var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: projectNames,
      datasets: [{
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
