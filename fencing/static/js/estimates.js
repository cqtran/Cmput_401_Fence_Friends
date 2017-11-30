var estimateTable = document.getElementById('estimateTable');

function uploadValues(e) {
  var message = 'Upload Prices File'
  console.log(message)
  var formdata = new FormData(document.getElementById("upload-form"));
  $.ajax({
      type: 'POST',
      url: '/uploadEstimates/',
      data : formdata,
      processData: false,
      contentType: false,
      success: function(response){
        console.log('good')
        refreshTable();
      }
  });
}

function getValues(categoryURL, category) {
  $.ajax({
      type: 'GET',
      url: categoryURL,
      success: function(result) {
          updateEstimateTable(result, category);
      },
      error: function(result) {
          showError(category);
      }
  });
}

function updateEstimateTable(result, category) {
  estimateTable.appendChild(makeHeader(category));
  table = makeTable();
  result.forEach(function(row) {
    table.appendChild(makeRow(row));
  });
  var final = document.createElement('div');
  final.appendChild(table);
  estimateTable.appendChild(final);
}

function makeTable() {
  // Returns a new table with table headers
  var table = document.createElement('table');
  table.setAttribute('class', 'table');
  var headerRow = document.createElement('tr');

  var col1 = document.createElement('th');
  col1.setAttribute('width', '50%');
  col1.innerHTML = 'Name';
  headerRow.appendChild(col1);

  var col2 = document.createElement('th');
  col2.setAttribute('width', '50%');
  col2.innerHTML = 'Value';
  headerRow.appendChild(col2);

  table.appendChild(headerRow);
  return table;
}

function makeHeader(string) {
  // Returns a new header
  var header = document.createElement('h4');
  header.setAttribute('class', 'text-green');
  header.setAttribute(
    'style', 'font-weight: bold; padding-top: 10px; cursor: pointer;');
  header.innerHTML = '<i class="fa fa-caret-down" aria-hidden="true"></i> ' + string;

  // Add accordion functionality to header classes
  header.onclick = function(){
    /* toggle if is shows */
    $(this).next().slideToggle();
    swapCaret(this);
  }

  return header;
}

function swapCaret(header) {
  var i = $(header).find('i:first');

  if (i.hasClass('fa-caret-down')) {
    i.removeClass('fa-caret-down');
    i.addClass('fa-caret-right');
  }

  else {
    i.removeClass('fa-caret-right');
    i.addClass('fa-caret-down');
  }
}

function makeRow(rowData) {
  // Returns a table row with data from the json object given
  var row = document.createElement('tr');

  var col1 = document.createElement('td');
  col1.setAttribute('width', '35%');
  col1.innerHTML = rowData.name;
  row.appendChild(col1);

  var col2 = document.createElement('td');
  col2.setAttribute('width', '15%');
  col2.innerHTML = rowData.value;
  row.appendChild(col2);

  return row;
}

function refreshTable() {
  $('#estimateTable').empty();
  getValues('/getStyleEstimates/', 'Style');
  getValues('/getColourEstimates/', 'Colour');
  getValues('/getHeightEstimates/', 'Height');
  getValues('/getGateEstimates/', 'Gate');
}

function showError(category) {
  // Show an error if there are no estimate values
  estimateTable.appendChild(makeHeader(category));
  var item = document.createElement('a');
  item.appendChild(document.createTextNode('No estimate values were found for ' + category));
  estimateTable.appendChild(item);
}

$(document).ready(function(){
  refreshTable()
});

$('#file-upload').change(function(){
  $('#upload-form').submit();
});

$('form').submit(function(e) {
  e.preventDefault();
  uploadValues(e);
});
