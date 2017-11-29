function getSummary() {
  $.ajax({
    type: 'GET',
    url: '/accounting/',
    success: function(result) {
      updateTable(result);
    },
    error: function(result) {
      showError();
    }
  });
}
function projectDeatils(){
  $.ajax({
      type: 'GET',
      url: '/projectdetails/' + proj_id,
      success: function(result) {

      },
      error: function(xhr, textStatus, error) {
    if (proj_id != null) {
      showMessage("Error");
    }
    
    console.log(xhr.statusText);
    console.log(textStatus);
    console.log(error);
      }
  });
}
function updateTable(row) {
  // Update the Accounting table with data
}

function showError() {
  var item = document.createElement('a');
  item.appendChild(document.createTextNode('Accounting summary not available'));
  // Append item to document
}

function update_quote_table(quotes) {
  var table = document.getElementById('tableBody');
  $('#tableBody').empty();
  quotes.forEach(function(quote) {
    // Insert each quote as a new table row
    table.appendChild(makeRow(quote));
  });
}

function makeRow(quote) {
    var row = document.createElement('tr');

    var project_id = document.createElement('td');
    project_id.innerHTML = quote.project_id
    row.appendChild(project_id);

    var project_id = document.createElement('td');
    project_id.innerHTML = '-'
    row.appendChild(project_id);

    var project_id = document.createElement('td');
    project_id.innerHTML = quote.amount
    row.appendChild(project_id);

    var project_id = document.createElement('td');
    project_id.innerHTML = quote.amount_gst
    row.appendChild(project_id);

    var project_id = document.createElement('td');
    var amount = parseFloat(quote.amount);
    var gst = parseFloat(quote.amount_gst);

    var total = amount + gst;
    var fixedtotal = total.toFixed(2)

    console.log(fixedtotal);

    project_id.innerHTML = fixedtotal


    row.appendChild(project_id);
    return row;
}
$(document).ready(function(){
  //pictureList = document.getElementById('projectPictures');
  $('#dataTable').DataTable({
      "ajax" :{
        "type": 'POST',
        "url": '/getAccountingSummary/',
      },
      "columns": [
        {"data": "quote_id"},
        {"data": "project_id"},
        {"data": "amount"},
        {"data": "amount_gst"},
        {"data": "amount"}
      ]
  });

  //getSummary();
  //getQuotes()
});
