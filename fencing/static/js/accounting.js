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


$(document).ready(function(){
  //pictureList = document.getElementById('projectPictures');

  // Suppress warnings so no warning on empty table
  $.fn.dataTable.ext.errMode = 'none';

  $('#dataTable').DataTable({
    "ajax" :{
      "type": 'POST',
      "url": '/getAccountingSummary/',
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


  $('#costTable').DataTable({
    "ajax" :{
      "type": 'POST',
      "url": '/getAccountingSummary/',
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

  // Remove "Search:" and add search icon
  var dataTableLabel = $('#dataTable_filter > label');
  dataTableLabel.html(dataTableLabel.children());            // Remove text
  dataTableLabel.prepend('<i class="fa fa-search"></i>');

  // Remove "Search:" and add search icon
  var dataTableLabel = $('#costTable_filter > label');
  dataTableLabel.html(dataTableLabel.children());            // Remove text
  dataTableLabel.prepend('<i class="fa fa-search"></i>');






  //getSummary();
});

function changePage(proj_id){
  window.location.href = '/projectinfo?proj_id=' + proj_id;
}

function slider(){
  /* toggle if is shows */
  console.log("tetsing");
  $(this).next().slideToggle();
  swapCaret(this);
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
