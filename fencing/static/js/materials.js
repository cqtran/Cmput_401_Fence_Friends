var priceTable = document.getElementById('priceTable');

function uploadPrices(e) {
  var message = 'Upload Prices File'
  console.log(message)
  var formdata = new FormData(document.getElementById("upload-form"));
  $.ajax({
      type: 'POST',
      url: '/uploadPrice/',
      data : formdata,
      processData: false,
      contentType: false,
      success: function(response){
        console.log('good')
        getPrices();
      }
  });
}

function getPrices() {
  // TODO: GET request to materials API to get prices list by year and create tables
  $.ajax({
      type: 'GET',
      url: '/getPriceList/',
      success: function(result) {
          updatePriceTable(result);
      },
      error: function(result) {
          showError();
      }
  });
}

function updatePriceTable(materialPrices) {
  $('#priceTable').empty();
  var lastCategory = '';
  var lastTable;
  materialPrices.forEach(function(material) {
    // Decide if the material is a new category
    if (material.category != lastCategory) {
      lastCategory = material.category;
      // Create a new header for the Category
      priceTable.appendChild(makeHeader(lastCategory));
      // Create a new table with table headers
      lastTable = makeTable();
      priceTable.appendChild(lastTable);
    }
    // Add the material as a new row in the table
    lastTable.appendChild(makeRow(material));
  });
}

function makeTable() {
  // Returns a new table with table headers
   var table = document.createElement('table');
   table.setAttribute('class', 'table')
   var headerRow = document.createElement('tr');

   var col1 = document.createElement('th');
   col1.setAttribute('width', '40%');
   col1.innerHTML = 'Material Name';
   headerRow.appendChild(col1);

   var col2 = document.createElement('th');
   col2.setAttribute('width', '15%');
   col2.innerHTML = 'My Price';
   headerRow.appendChild(col2);

   var col3 = document.createElement('th');
   col3.setAttribute('width', '15%');
   col3.innerHTML = 'Pieces in Bundle';
   headerRow.appendChild(col3);

   var col4 = document.createElement('th');
   col4.setAttribute('width', '30%');
   col4.innerHTML = 'Notes';
   headerRow.appendChild(col4);

   table.appendChild(headerRow);
   return table;
}

function makeHeader(string) {
  // Returns a new header
  var header = document.createElement('h4');
  header.setAttribute('class', 'text-green accordion');
  header.setAttribute('style', 'font-weight: bold; padding-top: 10px;');
  header.innerHTML = string;

  // Add accordion functionality to header classes
  // Source: https://www.w3schools.com/howto/howto_js_accordion.asp
  header.onclick = function(){
      /* Toggle between adding and removing the "active" class,
      to highlight the button that controls the panel */
      this.classList.toggle("active");

      /* Toggle between hiding and showing the active panel */
      var panel = this.nextElementSibling;
      if (panel.style.display === "block") {
          panel.style.display = "none";
      } else {
          panel.style.display = "block";
      }
  }
  return header;
}

function makeRow(material) {
  // Returns a table row with data from the json object given
  var row = document.createElement('tr')

  var col1 = document.createElement('td');
  col1.setAttribute('width', '35%');
  col1.innerHTML = material.material_name;
  row.appendChild(col1);

  var col2 = document.createElement('td');
  col2.setAttribute('width', '15%');
  col2.innerHTML = '$' + material.my_price;
  row.appendChild(col2);

  var col3 = document.createElement('td');
  col3.setAttribute('width', '20%');
  col3.innerHTML = material.pieces_in_bundle;
  row.appendChild(col3);

  var col4 = document.createElement('td');
  col4.setAttribute('width', '30%');
  col4.innerHTML = material.note;
  row.appendChild(col4);

  return row;
}

function showError() {
  // Show an error if there are no materials
  $('#priceTable').empty();
  var item = document.createElement('a');
  item.appendChild(document.createTextNode('No material prices were found. Upload a csv file of material prices'));
  priceTable.appendChild(item);
}

$(document).ready(function(){
  getPrices();
});

$('#file-upload').change(function(){
  $('#upload-form').submit();
});

$('form').submit(function(e) {
  e.preventDefault();
  uploadPrices(e);
});
