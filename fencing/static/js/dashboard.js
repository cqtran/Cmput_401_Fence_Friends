// -- Area Chart Example
var ctx;
var projectNames;
var projectProfit;
var myLineChart;

//sends an http request to return profit values
function getProfits(){
  $.ajax({
    type: 'POST',
    url: '/getProfit/',
    data: {'year': $('#year').val()},
    success: function(result) {
      projectProfit = [];
      projectNames = [];
      var profits = result["profits"];
      for(i = 0; i < profits.length; i++){
        if(i == 0){
          projectProfit.push(profits[i]);
        }
        else{
          var added = (parseFloat(profits[i]) + parseFloat(projectProfit[i-1])).toFixed('2');
          projectProfit.push(added);
        }
      }
      if(projectProfit.length >= 1){
        $('#total-profit').html('$' + projectProfit[projectProfit.length - 1]);
      }
      else{
        $('#total-profit').html('$0');
      }
      projectNames = result["projects"];
      makeChart();
    },
    error: function(result) {
        showMessage("Error getting profits");
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
    myLineChart.destroy();
    getProfits();
  });
});

//creates the line graph
function makeChart(){
  myLineChart = new Chart(ctx, {
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
function showMessage(message) {
  $('#message-text').html(message);
  $('#message').modal('show');
}