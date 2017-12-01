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


function extractData(){
  var rows = $('#dataTable').DataTable().rows().data();
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
  download("download.csv", export_file.join('\n'))}

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
      ]
  });

  // Remove "Search:" and add search icon
  var dataTableLabel = $('#dataTable_filter > label');
  dataTableLabel.html(dataTableLabel.children());            // Remove text
  dataTableLabel.prepend('<i class="fa fa-search"></i>');






  //getSummary();
});

function changePage(proj_id){
  window.location.href = '/projectinfo?proj_id=' + proj_id;
}
