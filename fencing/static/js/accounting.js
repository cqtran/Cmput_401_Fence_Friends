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

function getQuotes() {
  // TODO: GET request to materials API to get prices list by year and create tables
    console.log("good")
  $.ajax({
      type: 'GET',
      url: '/getAccountingSummary/',
      success: function(result) {
          console.log("we made it")
          update_quote_table(result);
      },
      error: function(result) {
          //showError();
          console.log('Error')
      }
  });
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

function exportTableToCSV($table, filename) {
                var $headers = $table.find('tr:has(th)')
                    ,$rows = $table.find('tr:has(td)')

                    // Temporary delimiter characters unlikely to be typed by keyboard
                    // This is to avoid accidentally splitting the actual contents
                    ,tmpColDelim = String.fromCharCode(11) // vertical tab character
                    ,tmpRowDelim = String.fromCharCode(0) // null character

                    // actual delimiter characters for CSV format
                    ,colDelim = '","'
                    ,rowDelim = '"\r\n"';

                    // Grab text from table into CSV formatted string
                    var csv = '"';
                    csv += formatRows($headers.map(grabRow));
                    csv += rowDelim;
                    csv += formatRows($rows.map(grabRow)) + '"';

                    // Data URI
                    var csvData = 'data:application/csv;charset=utf-8,' + encodeURIComponent(csv);

                // For IE (tested 10+)
                if (window.navigator.msSaveOrOpenBlob) {
                    var blob = new Blob([decodeURIComponent(encodeURI(csv))], {
                        type: "text/csv;charset=utf-8;"
                    });
                    navigator.msSaveBlob(blob, filename);
                } else {
                    $(this)
                        .attr({
                            'download': filename
                            ,'href': csvData
                            //,'target' : '_blank' //if you want it to open in a new window
                    });
                }

                //------------------------------------------------------------
                // Helper Functions
                //------------------------------------------------------------
                // Format the output so it has the appropriate delimiters
                function formatRows(rows){
                    return rows.get().join(tmpRowDelim)
                        .split(tmpRowDelim).join(rowDelim)
                        .split(tmpColDelim).join(colDelim);
                }
                // Grab and format a row from the table
                function grabRow(i,row){

                    var $row = $(row);
                    //for some reason $cols = $row.find('td') || $row.find('th') won't work...
                    var $cols = $row.find('td');
                    if(!$cols.length) $cols = $row.find('th');

                    return $cols.map(grabCol)
                                .get().join(tmpColDelim);
                }
                // Grab and format a column from the table
                function grabCol(j,col){
                    var $col = $(col),
                        $text = $col.text();

                    return $text.replace('"', '""'); // escape double quotes

                }
            }

$(document).ready(function(){
  //pictureList = document.getElementById('projectPictures');
  //$('#dataTable').DataTable();

  getSummary();
  getQuotes()
});
