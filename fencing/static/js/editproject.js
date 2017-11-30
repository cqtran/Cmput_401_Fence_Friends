var chosenCustomers = [];
var proj_id;
var statusList;

function showMessage(message) {
	$('#message-text').html(message);
	$('#message').modal('show');
}

function projectData(project){
  document.getElementById('project_name').value = project[0].project_name;
  document.getElementById('address').value = project[0].address;
  $('.selectpicker').selectpicker('val', project[0].status_name);
  document.getElementById('note').value = project[0].note;
  $('#companyNameNav').text(project[0].company_name);
  //add for loop for every customer once implemented
  getCustomer(project[0].customer_id);
}

function confirmDiscard() {
  return "Discard changes?";
}

function markDirty() {
  window.onbeforeunload = confirmDiscard;
}

function markClean() {
  window.onbeforeunload = null;
}
function getCustomer(cust_id){
  $.ajax({
    type: 'GET',
    url: '/getCustomer/' + cust_id,
    success: function(result) {
      addFirstToList(result[0]);
    }
  });
}
function getProjectData(){
//get details
  $.ajax({
      type: 'GET',
      url: '/getProject/' + proj_id,
      success: function(result) {
        projectData(result);
      }
  });
}
function deleteProject(){
  $.ajax({
      type: 'POST',
      url: '/deleteproject/',
      data: { 
          proj_id: proj_id,
      },
      datatype: 'json',
      success: function(result) {
          window.location.href = '/projects';
      },
      error: function(result) {
          showMessage('error');
      }
  });
}
function removeCust(customer, torem){
  return customer != torem;
}
//add customer to html
function addFirstToList(customer){
  //append to list of customers
  chosenCustomers.push(customer.customer_id);

  //get customer list element
  var customerList = document.getElementById('customers-list');

  $('#customers-list').append('\
  <div class="rounded customer-item container-fluid bottom-margin"> \
    <div class="col-12"> \
      <div class="row justify-content-between"> \
        <p class="top-bot-pad"><b>' + customer.first_name + '</b> - Phone ' + customer.cellphone + ' </p> \
        <button onclick="markDirty()" class="btn btn-grey float-right" type="button" id="' + customer.customer_id + '"> \
          <i class="fa fa-times" aria-hidden="true"></i> \
        </button> \
      </div> \
    </div> \
  </div>');
}
//add customer to html
function addToList(customer){
  if(chosenCustomers.length > 0){
    return;
  }
  //append to list of customers
  chosenCustomers.push(customer.cust_id);
  console.log(chosenCustomers);

  //get customer list element
  var customerList = document.getElementById('customers-list');

  $('#customers-list').append('\
  <div class="rounded customer-item container-fluid bottom-margin"> \
    <div class="col-12"> \
      <div class="row justify-content-between"> \
        <p class="top-bot-pad"><b>' + customer.value + '</b> - Phone ' + customer.phone + ' </p> \
        <button class="btn btn-grey float-right" type="button" id="' + customer.cust_id + '"> \
          <i class="fa fa-times" aria-hidden="true"></i> \
        </button> \
      </div> \
    </div> \
  </div>');
}
//delete html customer item on click
$(document).on('click', '.btn-grey', function(e) {
  var cid = this.id;
  chosenCustomers = chosenCustomers.filter(removeCust.bind(this, cid));
  $(e.target).parent().parent().parent().remove();
});

//send request to create project
$('#edit-form').submit(function(e) {
  e.preventDefault();
  markClean();
  console.log(chosenCustomers);
  if(typeof chosenCustomers != "undefined" && chosenCustomers != null && chosenCustomers.length > 0){
    $.ajax({
        type: 'POST',
        url: '/updateproject/',
        data: { 
            customer: JSON.stringify(chosenCustomers), // < note use of 'this' here
            name: $("#project_name").val(),
            status: $("#status").val(),
            proj_id: proj_id,
            note: $("#note").val(),
            address: $('#address').val()
        },
        datatype: 'json',
        success: function(result) {
            window.location.href = '/projectinfo?proj_id=' + proj_id;
        },
        error: function(result) {
            showMessage('error');
        }
    });
  }
  else {
    showMessage("A customer must be selected.");
  }
});

//populate typeahead with customers
$('#add-project .typeahead').typeahead({
    highlight: true
  },
  {
    name: 'customers',
    displayKey: 'value',
    source: customers.ttAdapter(),
    templates: {
        suggestion: Handlebars.compile("<div class='container-fluid'><p class='top-bot-pad'><b>{{value}}</b> - Phone {{phone}} </p></div>")
    }
  }).on('typeahead:selected', function(event, selection) {
  if(!chosenCustomers.includes(selection.cust_id)){
    addToList(selection);
  }
});

//this runs after the html has loaded, all function calls should be in here
$(document).ready(function(){
  statusList = document.getElementById('status');
  proj_id = getParameterByName('proj_id');
  if(proj_id == null) {
    $('#message').on('hidden.bs.modal', function() {
      window.location.href = '/projects/';
    });
  
    showMessage("Project does not exist.");
  }
  getStatus();
  getProjectData();
});

$('#delete-project').click(function(){
  deleteProject();
});