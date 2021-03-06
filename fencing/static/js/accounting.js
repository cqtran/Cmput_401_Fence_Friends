var tableCost;
var tableData;

function getSummary() {
  $.ajax({
    type: 'GET',
    url: '/accounting/',
    success: function(result) {
      updateTable(result);
    },
    error: function(result) {
      showMessage("Data not available.")
    }
  });
}
function updateTable(row) {
  // Update the Accounting table with data
}

function extractData(tablename, filename){
  var rows = $(tablename).DataTable().rows().data();
  var export_file = [];
  var row;
  export_file.push("Job Number,Description,Amount,GST,Total");
  for(var i = 0; i< rows.length; i++ ){
      row = [];
      row.push(rows[i]['quote_id']);
      row.push(rows[i]['project_id']);
      row.push(rows[i]['amount']);
      row.push(rows[i]['amount_gst']);
      row.push(rows[i]['amount']);
      export_file.push(row.join(','));



}
  download(filename + ".csv", export_file.join('\n'))}

function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

//populate years in dropdown
function yearSelect(){
  for (i = new Date().getFullYear(); i > 2015; i--) {
    $('select[name=dataYear]').append('<option value="' + i + '">' + i + '</option>');
    $('select[name=costYear]').append('<option value="' + i + '">' + i + '</option>');
  }
  $('.selectpicker').selectpicker('refresh');
}

function populateData(){
  //populate data for data table
  tableData = $('#dataTable').DataTable({
    searching: false,
    "ajax" :{
      "type": 'POST',
      "url": '/getAccountingSummary/',
      "data": function ( d ) {
        d.year = $('#dataYear').val();
    },
    },
    "columns": [
      {"data": "quote_id"},
      {"data": "project_id",
        "render": function(data, type, row, meta){
          if(type === 'display'){
              data = '<a onclick="changePage(' + data + ')" class="link-to-project">' + data + '</a>';
          }

          return data;
        }
      },
      {"data": "amount"},
      {"data": "amount_gst"},
      {"data": "amount_total"}
    ],
    "footerCallback": function ( row, data, start, end, display ) {
      var api = this.api(), data;

      // Remove the formatting to get integer data for summation
      var intVal = function ( i ) {
          return typeof i === 'string' ?
              i.replace(/[\$,]/g, '')*1 :
              typeof i === 'number' ?
                  i : 0;
      };

      // Total over all pages
      revenueTotal = api
          .column(2)
          .data()
          .reduce( function (a, b) {
              return intVal(a) + intVal(b);
          }, 0 );
      // Total over all pages
      gstTotal = api
          .column(3)
          .data()
          .reduce( function (a, b) {
              return intVal(a) + intVal(b);
          }, 0 );
      // Total over all pages
      customerTotal = api
          .column(4)
          .data()
          .reduce( function (a, b) {
              return intVal(a) + intVal(b);
          }, 0 );
      // Update footer
      $( api.column(2).footer() ).html('$'+ revenueTotal.toFixed('2'));
      $( api.column(3).footer() ).html('$'+ gstTotal.toFixed('2'));
      $( api.column(4).footer() ).html('$'+ customerTotal.toFixed('2'));
    }
  });
}

function populateCost(){
  //populate data for cost table
  tableCost = $('#costTable').DataTable({
    searching: false,
    "ajax" :{
      "type": 'POST',
      "url": '/getAccountingSummary/',
      "data": function ( d ) {
        d.year = $('#costYear').val();
    },
    },
    "columns": [
      {"data": "quote_id"},
      {"data": "project_id",
        "render": function(data, type, row, meta){
          if(type === 'display'){
              data = '<a onclick="changePage(' + data + ')" class="link-to-project">' + data + '</a>';
          }

          return data;
        }
      },
      {"data": "material_expense"},
      {"data": "material_expense_gst"},
      {"data": "material_expense_total"}
    ],
    "footerCallback": function ( row, data, start, end, display ) {
      var api = this.api(), data;

      // Remove the formatting to get integer data for summation
      var intVal = function ( i ) {
          return typeof i === 'string' ?
              i.replace(/[\$,]/g, '')*1 :
              typeof i === 'number' ?
                  i : 0;
      };

      // Total over all pages
      revenueTotal = api
          .column(2)
          .data()
          .reduce( function (a, b) {
              return intVal(a) + intVal(b);
          }, 0 );
      // Total over all pages
      gstTotal = api
          .column(3)
          .data()
          .reduce( function (a, b) {
              return intVal(a) + intVal(b);
          }, 0 );
      // Total over all pages
      customerTotal = api
          .column(4)
          .data()
          .reduce( function (a, b) {
              return intVal(a) + intVal(b);
          }, 0 );
      // Update footer
      $( api.column(2).footer() ).html('$'+ revenueTotal.toFixed('2'));
      $( api.column(3).footer() ).html('$'+ gstTotal.toFixed('2'));
      $( api.column(4).footer() ).html('$'+ customerTotal.toFixed('2'));
    }
  });
}
$(document).ready(function(){
  yearSelect();

  // Suppress warnings so no warning on empty table
  $.fn.dataTable.ext.errMode = 'none';

  populateData();
  populateCost();

  // Remove "Search:" and add search icon
  var dataTableLabel = $('#dataTable_filter > label');
  dataTableLabel.html(dataTableLabel.children());            // Remove text
  dataTableLabel.prepend('<i class="fa fa-search"></i>');

  // Remove "Search:" and add search icon
  var dataTableLabel = $('#costTable_filter > label');
  dataTableLabel.html(dataTableLabel.children());            // Remove text
  dataTableLabel.prepend('<i class="fa fa-search"></i>');

  //onclick listener for sliding
  $('.slidey').click(function(){
    slider(this);
  })
  $('#dataYear').on('change', function() {
    tableData.clear().draw();
    tableData.ajax.reload();
  });
  $('#costYear').on('change', function() {
    tableCost.clear().draw();
    tableCost.ajax.reload();
  });
});

//change to projectinfo
function changePage(proj_id){
  window.location.href = '/projectinfo?proj_id=' + proj_id;
}

//these deal with hiding the charts
function slider(item){
  /* toggle if is shows */
  $(item).next().next().slideToggle();
  swapCaret(item);
}
function swapCaret(header) {
  var i = $(header).find('i:first');

  if (i.hasClass('fa-caret-down')) {
    i.removeClass('fa-caret-down');
    i.addClass('fa-caret-left');
  }

  else {
    i.removeClass('fa-caret-left');
    i.addClass('fa-caret-down');
  }
}
function showMessage(message) {
  $('#message-text').html(message);
  $('#message').modal('show');
}
